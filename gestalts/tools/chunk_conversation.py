
import argparse, os, re, json, hashlib, datetime as dt
from typing import List, Dict, Any, Tuple

def approx_token_count(text: str) -> int:
    # Rough heuristic: ~4 chars per token (English). Safer than relying on external libs.
    # Users can switch to --max-chars to control by characters instead.
    return max(1, int(len(text) / 4))

def sha1(text: str) -> str:
    import hashlib
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:10]

def read_plain(path: str) -> List[Dict[str, Any]]:
    # Split into message-like blocks (double newlines as separators)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()
    # Try to detect simple "Role: " prefixes; otherwise mark as "unknown"
    blocks = re.split(r"\n{2,}", data.strip())
    messages = []
    for b in blocks:
        m = re.match(r"^(user|assistant|system)\s*:\s*(.*)$", b.strip(), flags=re.I|re.S)
        if m:
            role = m.group(1).lower()
            content = m.group(2).strip()
        else:
            role = "unknown"
            content = b.strip()
        messages.append({"role": role, "content": content})
    return messages

def read_jsonl(path: str) -> List[Dict[str, Any]]:
    msgs = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                role = obj.get("role", "unknown")
                content = obj.get("content", "")
                ts = obj.get("timestamp")
                msgs.append({"role": role, "content": content, "timestamp": ts})
            except Exception:
                # Fallback: treat as plaintext chunk
                msgs.append({"role": "unknown", "content": line})
    return msgs

def split_long_message(msg: Dict[str, Any], max_tokens: int) -> List[Dict[str, Any]]:
    # Split by paragraphs then sentences to fit max_tokens
    content = msg["content"]
    role = msg.get("role", "unknown")
    ts = msg.get("timestamp")
    parts = []
    paragraphs = re.split(r"\n{2,}", content)
    buf = ""
    for para in paragraphs:
        if approx_token_count(buf + ("\n\n" if buf else "") + para) <= max_tokens:
            buf = (buf + ("\n\n" if buf else "") + para) if buf else para
        else:
            # split para by sentence-ish boundaries
            sentences = re.split(r"(?<=[.!?…])\s+", para)
            for s in sentences:
                if approx_token_count((buf + " " + s).strip()) <= max_tokens:
                    buf = (buf + " " + s).strip() if buf else s
                else:
                    if buf:
                        parts.append({"role": role, "content": buf, "timestamp": ts})
                    buf = s
    if buf:
        parts.append({"role": role, "content": buf, "timestamp": ts})
    return parts

def chunk_messages(messages: List[Dict[str, Any]], max_tokens: int, overlap_tokens: int) -> Tuple[List[str], List[Dict[str, Any]]]:
    chunks = []
    manifests = []
    current: List[Dict[str, Any]] = []
    current_tokens = 0

    def flush_chunk():
        nonlocal current, current_tokens
        if not current:
            return None
        text = "\n\n".join([f"{m.get('role','unknown')}: {m['content']}".strip() for m in current])
        chunks.append(text)
        manifests.append({
            "messages": len(current),
            "token_estimate": approx_token_count(text),
            "sha1": sha1(text),
        })
        # Build overlap buffer
        if overlap_tokens > 0:
            # Take from the tail until we reach ~overlap_tokens
            overlap = []
            t = 0
            for m in reversed(current):
                mtok = approx_token_count(m["content"])
                overlap.insert(0, m)
                t += mtok
                if t >= overlap_tokens:
                    break
            current = overlap[:]  # start next chunk with overlap
            current_tokens = sum(approx_token_count(m["content"]) for m in current)
        else:
            current = []
            current_tokens = 0

    for msg in messages:
        mtok = approx_token_count(msg.get("content",""))
        if mtok > max_tokens:
            # Split this message first
            parts = split_long_message(msg, max_tokens=max(1, max_tokens-1))
        else:
            parts = [msg]

        for part in parts:
            p_tokens = approx_token_count(part.get("content",""))
            if current_tokens + p_tokens > max_tokens and current:
                flush_chunk()
            current.append(part)
            current_tokens += p_tokens

    if current:
        flush_chunk()

    return chunks, manifests

def guess_format(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".jsonl", ".ndjson"]:
        return "jsonl"
    return "plain"

def write_chunks(chunks: List[str], manifests: List[Dict[str, Any]], outdir: str, base_slug: str, date_hint: str = None):
    os.makedirs(outdir, exist_ok=True)
    date_str = date_hint or dt.datetime.utcnow().strftime("%Y-%m-%d")
    index = []
    for i, (text, meta) in enumerate(zip(chunks, manifests), start=1):
        fname = f"{date_str}_{base_slug}_{i:03d}.md"
        path = os.path.join(outdir, fname)
        header = f"""---
title: {base_slug.replace('_',' ').title()} · Part {i}
date: {date_str}
part_index: {i}
parts_total: {len(chunks)}
token_estimate: {meta['token_estimate']}
sha1: {meta['sha1']}
---
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + "\n" + text + "\n")
        index.append({
            "file": fname,
            "sha1": meta["sha1"],
            "token_estimate": meta["token_estimate"],
        })
    # Write manifest
    manifest_path = os.path.join(outdir, f"{date_str}_{base_slug}_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as mf:
        json.dump({
            "base_slug": base_slug,
            "date": date_str,
            "parts": index
        }, mf, indent=2)
    return manifest_path

def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip().lower())
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "conversation"

def main():
    ap = argparse.ArgumentParser(description="Split long conversations into chunks with overlap.")
    ap.add_argument("input", help="Path to input file (plain text/markdown or JSONL).")
    ap.add_argument("--max-tokens", type=int, default=1800, help="Approx token limit per chunk (heuristic 4 chars/token).")
    ap.add_argument("--overlap-tokens", type=int, default=120, help="Approx tokens to overlap between chunks (0 to disable).")
    ap.add_argument("--max-chars", type=int, default=None, help="Use char-based limit instead of tokens.")
    ap.add_argument("--outdir", default="chunks_out", help="Output directory.")
    ap.add_argument("--slug", default=None, help="Base slug for filenames; defaults to input stem.")
    ap.add_argument("--date", default=None, help="Date string YYYY-MM-DD for filenames/frontmatter.")
    args = ap.parse_args()

    fmt = guess_format(args.input)
    if fmt == "jsonl":
        messages = read_jsonl(args.input)
    else:
        messages = read_plain(args.input)

    # Optional char-based chunking: convert to pseudo-token counts (1 token = 4 chars)
    if args.max_chars is not None:
        max_tokens = max(1, int(args.max_chars / 4))
    else:
        max_tokens = args.max_tokens

    overlap_tokens = max(0, int(args.overlap_tokens))

    # Ensure messages list isn't empty
    messages = [m for m in messages if str(m.get("content","")).strip()]
    if not messages:
        print("No messages found.")
        return

    base_slug = args.slug or slugify(os.path.splitext(os.path.basename(args.input))[0])

    chunks, manifests = chunk_messages(messages, max_tokens=max_tokens, overlap_tokens=overlap_tokens)
    manifest_path = write_chunks(chunks, manifests, args.outdir, base_slug=base_slug, date_hint=args.date)

    print(f"Wrote {len(chunks)} chunks to {args.outdir}")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
