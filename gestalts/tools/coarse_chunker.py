
#!/usr/bin/env python3
import re, json
from pathlib import Path
from typing import List, Dict, Tuple

MSG_RE = re.compile(r"^\[(\d{5})\](\w+)\(([^)]+)\):(.*)$")

def read_messages(path: str) -> List[Dict]:
    raw = Path(path).read_text(encoding="utf-8")
    blocks, cur = [], []
    for line in raw.splitlines(True):
        if line.strip() == "":
            if cur:
                blocks.append("".join(cur).strip()); cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append("".join(cur).strip())

    messages = []
    for i, block in enumerate(blocks):
        first = block.splitlines()[0].strip()
        m = MSG_RE.match(first)
        mid = int(m.group(1)) if m else None
        speaker = m.group(2) if m else None
        ts = m.group(3) if m else None
        messages.append({
            "idx": i,
            "id": mid,
            "speaker": speaker,
            "timestamp": ts,
            "raw": block,
        })
    return messages

def chunk_by_limits(messages: List[Dict], max_messages: int = 200, max_chars: int = None, overlap_messages: int = 20):
    """
    Coarse chunking by message count and/or character budget.
    Overlaps are applied by repeating the last `overlap_messages` in the next chunk.
    Splits always occur on message boundaries.
    """
    chunks = []
    n = len(messages)
    start_idx = 0
    while start_idx < n:
        end_idx = start_idx
        char_count = 0

        while end_idx < n:
            next_len = len(messages[end_idx]["raw"]) + 2  # include blank line separator
            next_count = (end_idx - start_idx + 1)
            if max_messages and next_count > max_messages:
                break
            if max_chars and (char_count + next_len) > max_chars:
                break
            char_count += next_len
            end_idx += 1

        # If we didn't advance (e.g., single message too large), force include at least one
        if end_idx == start_idx:
            end_idx = min(n, start_idx + 1)

        chunk = messages[start_idx:end_idx]
        # Determine overlap-aware next start
        if overlap_messages > 0:
            next_start = max(start_idx + len(chunk) - overlap_messages, start_idx + 1)
        else:
            next_start = end_idx
        chunks.append({
            "start_idx": start_idx,
            "end_idx": end_idx - 1,
            "messages": chunk
        })
        if end_idx >= n:
            break
        start_idx = next_start

    return chunks

def write_chunks(chunks, out_dir: str, prompt_template: str = None):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"chunks": [], "prompt_template": None}

    for i, ch in enumerate(chunks, start=1):
        msgs = ch["messages"]
        text = "\n\n".join(m["raw"] for m in msgs)
        ids = [m["id"] for m in msgs if m["id"] is not None]
        start_id = ids[0] if ids else None
        end_id = ids[-1] if ids else None
        fname = out / f"coarse_chunk_{i:03d}.txt"
        fname.write_text(text, encoding="utf-8")

        manifest["chunks"].append({
            "chunk_index": i,
            "file": fname.name,
            "message_range": [start_id, end_id],
            "message_index_range": [ch["start_idx"], ch["end_idx"]],
            "message_count": len(msgs),
            "char_count": len(text),
        })

        if prompt_template:
            prompt = prompt_template.format(first_id=start_id, last_id=end_id, slice_text=text)
            (out / f"coarse_chunk_{i:03d}_prompt.txt").write_text(prompt, encoding="utf-8")

    if prompt_template:
        manifest["prompt_template"] = prompt_template

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest

DEFAULT_PROMPT = """You are given a slice of a conversation as numbered messages like:
[00025]Name(ISO8601): text

Your task: split THIS SLICE ONLY into 20–50 message chunks by topic/emotional flow.

Rules:
- Use the numbers inside [] as the ONLY message IDs. Strip leading zeros in output.
- Do NOT invent or renumber messages. The chunk_range must be within [{first_id}, {last_id}] in this slice.
- Overlap is allowed and encouraged if a transition spans the boundary.
- Prefer natural scene ends; allow a shorter final chunk in this slice if needed.
- Output JSON ONLY: a list of objects with fields:
  - "chunk_range": [start_id, end_id]  (IDs from [])
  - "summary": 2–3 sentences
  - "reason_for_boundary": brief reason

Return chunks ONLY for this slice.
Conversation slice:
```
{slice_text}
```"""

def run_coarse_chunking(conversation_path: str, out_dir: str,
                        max_messages: int = 200, max_chars: int = None, overlap_messages: int = 20,
                        write_prompts: bool = True):
    messages = read_messages(conversation_path)
    chunks = chunk_by_limits(messages, max_messages=max_messages, max_chars=max_chars,
                             overlap_messages=overlap_messages)
    manifest = write_chunks(chunks, out_dir, DEFAULT_PROMPT if write_prompts else None)
    return manifest

if __name__ == "__main__":
    # basic CLI-free run; edit parameters here or import and call run_coarse_chunking
    conv = "conversation.txt"
    out = "coarse_chunks"
    # Tune these defaults if you need smaller slices for your model limits
    manifest = run_coarse_chunking(conv, out, max_messages=180, max_chars=None, overlap_messages=12, write_prompts=True)
    print(json.dumps(manifest, indent=2))
