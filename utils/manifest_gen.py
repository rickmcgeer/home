import hashlib
import json
from pathlib import Path
import sys

def extract_metadata(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        contents = f.read()

    # Compute hash
    file_hash = hashlib.sha256(contents.encode("utf-8")).hexdigest()

    # Extract lines
    lines = contents.splitlines()
    metadata = {"title": "", "tier": None, "tags": []}

    for line in lines:
        if line.startswith("Title:"):
            metadata["title"] = line.split(":", 1)[1].strip()
        elif line.startswith("Tier:"):
            metadata["tier"] = int(line.split(":", 1)[1].strip())
        elif line.startswith("Tags:"):
            metadata["tags"] = [tag.strip() for tag in line.split(":", 1)[1].split(",")]

    # Extract date from filename
    date_str = Path(file_path).name.split("_")[0]

    return {
        "path": f"vault/gestalts/{Path(file_path).name.replace('.md.md', '.md')}",
        "title": metadata["title"],
        "date": date_str,
        "tier": metadata["tier"],
        "tags": metadata["tags"],
        "hash": file_hash
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python manifest_gen.py <path-to-md-file>")
        return

    file_path = sys.argv[1]
    manifest_entry = extract_metadata(file_path)
    print(json.dumps(manifest_entry, indent=2))

if __name__ == "__main__":
    main()
