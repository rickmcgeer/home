import subprocess
import time
from pathlib import Path
import json
import hashlib
import sys

GESTALT_DIR = Path("vault/gestalts")
MANIFEST_PATH = Path("vault/manifest.json")
CHECK_INTERVAL = 10  # seconds

def compute_hash(file_path):
    contents = file_path.read_text(encoding="utf-8")
    return hashlib.sha256(contents.encode("utf-8")).hexdigest()

def parse_metadata(file_path):
    lines = file_path.read_text(encoding="utf-8").splitlines()
    metadata = {"title": "", "tier": None, "tags": []}
    for line in lines:
        if line.startswith("Title:"):
            metadata["title"] = line.split(":", 1)[1].strip()
        elif line.startswith("Tier:"):
            metadata["tier"] = int(line.split(":", 1)[1].strip())
        elif line.startswith("Tags:"):
            metadata["tags"] = [tag.strip() for tag in line.split(":", 1)[1].split(",")]
    return metadata

def load_manifest():
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_manifest(entries):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

def scan_and_commit():
    manifest = load_manifest()
    seen_paths = {entry["path"] for entry in manifest}

    for file_path in GESTALT_DIR.glob("*.md"):
        rel_path = str(file_path).replace("\\", "/")
        if rel_path not in seen_paths:
            meta = parse_metadata(file_path)
            file_hash = compute_hash(file_path)
            date_str = file_path.name.split("_")[0]
            entry = {
                "path": rel_path,
                "title": meta["title"],
                "date": date_str,
                "tier": meta["tier"],
                "tags": meta["tags"],
                "hash": file_hash
            }
            print(f"💾 New gestalt detected: {rel_path}")
            manifest.append(entry)
            save_manifest(manifest)
            subprocess.run(["git", "add", str(file_path), str(MANIFEST_PATH)])
            subprocess.run(["git", "commit", "-m", f"Add gestalt {file_path.name}"])
            print("✅ Committed to git.")

def main():
    print("👁️ Watching for new gestalts...")
    while True:
        try:
            scan_and_commit()
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("🛑 Stopped.")
            break

if __name__ == "__main__":
    main()