
#!/usr/bin/env python3
"""
Stitch fine-chunk outputs (JSON) from overlapping coarse slices into a single, ordered set.
- Deduplicates near-identical chunk ranges across slices
- Drops fully contained duplicates
- Optionally merges overlapping/adjacent ranges when they are "similar enough"
- Runs structural QA at the end

Expected input:
  A directory containing one or more JSON files, each of which is a list of objects like:
    { "chunk_range": [start_id, end_id], "summary": "...", "reason_for_boundary": "..." }

Usage:
  python stitch_fine_chunks.py --in_dir fine_chunks_dir --out stitched_full_chunks.json
"""

import os, json, argparse
from pathlib import Path
from typing import List, Dict, Tuple

def load_chunks(in_dir: str) -> List[Dict]:
    items: List[Dict] = []
    for p in Path(in_dir).glob("*.json"):
        # Skip obvious non-chunk files
        if p.name.lower().startswith(("manifest", "full-chunks")):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, list) and data and isinstance(data[0], dict) and "chunk_range" in data[0]:
                items.extend(data)
        except Exception as e:
            # Non-fatal; continue
            pass
    return items

def iou(a: Tuple[int,int], b: Tuple[int,int]) -> float:
    (as_, ae) = a; (bs, be) = b
    inter = max(0, min(ae, be) - max(as_, bs) + 1)
    union = (ae - as_ + 1) + (be - bs + 1) - inter
    return inter/union if union > 0 else 0.0

def overlap_len(a: Tuple[int,int], b: Tuple[int,int]) -> int:
    (as_, ae) = a; (bs, be) = b
    return max(0, min(ae, be) - max(as_, bs) + 1)

def sort_chunks(chunks: List[Dict]) -> List[Dict]:
    return sorted(chunks, key=lambda c: (c["chunk_range"][0], c["chunk_range"][1]))

def drop_contained(sorted_chunks: List[Dict]) -> List[Dict]:
    out: List[Dict] = []
    for ch in sorted_chunks:
        cs, ce = ch["chunk_range"]
        contained = False
        for kept in out:
            ks, ke = kept["chunk_range"]
            if cs >= ks and ce <= ke:
                contained = True
                break
        if not contained:
            out.append(ch)
    return out

def merge_similar(sorted_chunks: List[Dict], iou_threshold=0.6, allow_union=True) -> List[Dict]:
    """
    Merge chunks that are likely the same boundary discovered in overlapping slices.
    If IoU >= threshold, we treat them as the same and keep the unioned range (safer).
    """
    if not sorted_chunks:
        return []
    merged: List[Dict] = [sorted_chunks[0]]
    for ch in sorted_chunks[1:]:
        prev = merged[-1]
        a = tuple(prev["chunk_range"])
        b = tuple(ch["chunk_range"])
        score = iou(a, b)
        if score >= iou_threshold:
            # Merge by union (min start, max end)
            new_range = [min(a[0], b[0]), max(a[1], b[1])] if allow_union else [max(a[0], b[0]), min(a[1], b[1])]
            # Combine notes/summaries succinctly
            def combine(a_str, b_str):
                if not a_str: return b_str
                if not b_str: return a_str
                if b_str in a_str: return a_str
                return a_str.rstrip(". ") + " | " + b_str
            prev["chunk_range"] = new_range
            prev["summary"] = combine(prev.get("summary",""), ch.get("summary",""))
            prev["reason_for_boundary"] = combine(prev.get("reason_for_boundary",""), ch.get("reason_for_boundary",""))
        else:
            merged.append(ch)
    return merged

def qa_check_chunks(chunks: List[Dict], min_size=20, max_size=60,
                    max_gap=0, require_overlap=True, allow_short_final=True, min_overlap=1) -> List[str]:
    warnings, prev_end = [], None
    for i, ch in enumerate(chunks):
        start, end = ch["chunk_range"]
        size = end - start + 1
        if start > end:
            warnings.append(f"Chunk {i+1} has start > end: {start} > {end}")
        if size < min_size and not (allow_short_final and i == len(chunks)-1):
            warnings.append(f"Chunk {i+1} too small: {size} (min {min_size})")
        if size > max_size:
            warnings.append(f"Chunk {i+1} too large: {size} (max {max_size})")
        if prev_end is not None:
            gap = start - prev_end - 1
            overlap = max(0, prev_end - start + 1)
            if gap > max_gap:
                warnings.append(f"Gap of {gap} messages before chunk {i+1}")
            if require_overlap and overlap < min_overlap:
                warnings.append(f"Insufficient overlap ({overlap}) before chunk {i+1}; need ≥ {min_overlap}")
        prev_end = end
    return warnings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_dir", required=True, help="Directory with fine-chunk JSON files")
    ap.add_argument("--out", default="stitched_full_chunks.json", help="Output JSON path")
    ap.add_argument("--iou", type=float, default=0.6, help="IoU threshold to consider chunks the same")
    ap.add_argument("--min_size", type=int, default=20)
    ap.add_argument("--max_size", type=int, default=60)
    ap.add_argument("--allow_short_final", action="store_true", default=True)
    ap.add_argument("--require_overlap", action="store_true", default=True)
    ap.add_argument("--min_overlap", type=int, default=1)
    args = ap.parse_args()

    chunks = load_chunks(args.in_dir)
    if not chunks:
        print("No fine-chunk files found with the expected schema.")
        return

    # Normalize ranges to int and sort
    for ch in chunks:
        ch["chunk_range"] = [int(ch["chunk_range"][0]), int(ch["chunk_range"][1])]
        ch.setdefault("summary", "")
        ch.setdefault("reason_for_boundary", "")

    sorted_once = sort_chunks(chunks)
    without_contained = drop_contained(sorted_once)
    merged = merge_similar(without_contained, iou_threshold=args.iou, allow_union=True)
    merged = sort_chunks(merged)

    # QA
    warnings = qa_check_chunks(merged, min_size=args.min_size, max_size=args.max_size,
                               require_overlap=args.require_overlap,
                               allow_short_final=args.allow_short_final,
                               min_overlap=args.min_overlap)

    Path(args.out).write_text(json.dumps(merged, indent=2), encoding="utf-8")
    print(f"Wrote stitched chunks → {args.out} ({len(merged)} chunks)")
    if warnings:
        print("\nQA warnings:")
        for w in warnings: print(" -", w)
    else:
        print("\nAll checks passed ✅")

if __name__ == "__main__":
    main()
