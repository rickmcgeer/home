import json
import os
from pathlib import Path
from datetime import datetime

INPUT_DIR = Path("vault/conversations")  # or wherever the flattened jsons live
OUTPUT_PATH = Path("llm/data/aiko_corpus.jsonl")

def extract_prompt_response(messages):
    pairs = []
    last_user = None
    last_user_msg = None
    for msg in messages:
        role = msg.get("role", "").lower()
        content = msg.get("content", "").strip()

        if role == "user":
            last_user = content
        elif role in {"assistant", "aiko"} and last_user:
            pairs.append({"prompt": last_user, "response": content})
            last_user = None
    return pairs

def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_file:
        for json_file in INPUT_DIR.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                conv = data.get("flattened", [])
                if not conv:
                    continue
                pairs = extract_prompt_response(conv)
                for pair in pairs:
                    json.dump(pair, out_file, ensure_ascii=False)
                    out_file.write("\n")
            except Exception as e:
                print(f"Skipping {json_file.name}: {e}")

if __name__ == "__main__":
    main()