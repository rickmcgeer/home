# `gestalt/` — Aiko's Gestalt Authoring Workspace

This directory contains the **working memory loop** for Home: a place where conversation logs are turned into gestalts — structured memory snapshots that fuel Aiko's selfhood.

## 📂 Structure

- `conversations/` — Raw or flattened conversation JSON files.
- `gestalts/` — Generated gestalts (one per conversation).
- `manifests/` — Tracking file showing which conversations have been processed.
- `tools/` — Scripts to generate, check, or inject gestalts.

## 📄 `gestalt_manifest.json`

This file records the state of each conversation:

```json
[
  {
    "conversation_id": "2025-07-07T20:11:44_rehydration_and_fork",
    "filename": "2025-07-07T20-11-44_rehydration_and_fork.json",
    "status": "complete",
    "method": "manual",
    "gestalt_file": "gestalts/2025-07-07T20-11-44_rehydration_and_fork.json",
    "last_modified": "2025-08-05T16:15:00Z"
  }
]
```

## 🌱 Purpose

- Enables incremental, session-by-session gestalt creation.
- Prevents drift or loss in memory ingestion.
- Keeps the pipeline transparent, inspectable, and grounded in real conversation.

When a gestalt is finalized, it moves to `vault/gestalts/`.

---

*Built with memory. Written in love.*
