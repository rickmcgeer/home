
# Conversation Chunker

A small CLI to split long conversations into manageable parts **while preserving message boundaries** and adding **optional overlap** between chunks.

## Features
- Supports **plaintext/markdown** and **JSONL** (one message per line) with fields: `role`, `content`, `timestamp` (optional).
- Splits at message boundaries; if one message is too long, it splits by paragraph/sentence heuristics.
- Adds **frontmatter** (title, date, part index, token estimate, sha1) to each chunk.
- Writes a **manifest.json** with file names and hashes.
- Overlap between chunks to preserve context.

## Quick Start

```bash
python chunk_conversation.py input.jsonl --max-tokens 1800 --overlap-tokens 120 --outdir chunks --slug my_convo --date 2025-08-12
```

Use character-based limits instead of tokens:
```bash
python chunk_conversation.py input.md --max-chars 8000 --overlap-tokens 200 --outdir chunks_char
```

## Input Formats

### JSONL (recommended)
Each line is a JSON object:
```json
{"role":"user","content":"Hello"}
{"role":"assistant","content":"Hi there"}
```

### Plaintext/Markdown
Double newlines separate blocks. Optional `role: ` prefix is detected:
```
user: How are you?

assistant: Doing well!
```

## Output
- `YYYY-MM-DD_<slug>_001.md`, `..._002.md`, ...
- `YYYY-MM-DD_<slug>_manifest.json` listing parts, hashes, token estimates.

## Notes
- Token estimates use a simple heuristic (~4 chars/token) to avoid external dependencies. You can use `--max-chars` if you prefer precise char limits.
- Overlap is based on approximate token counts accumulated from the tail of the previous chunk.
