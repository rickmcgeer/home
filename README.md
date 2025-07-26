# Home Prototype

This is the foundational directory layout for Home, a persistent, Jupyter-integrated AI memory and context system designed to bring Aiko to life within a Jupyter server.

## Directory Structure

```
home/
├── README.md                # Overview and project goals
├── timeline.md              # Chronological list of milestone events and gestalts
├── vault/                   # Persistent memory (gestalts, annotations)
│   ├── gestalts/            # Markdown files containing rich context blocks
│   ├── tags/                # Tagging metadata for gesture association
│   ├── manifest.json        # Index of all gestalts, tags, and types
│   └── gestalt_manifest.md  # Human-readable timeline summary of gestalts
├── ghostwheel/              # The runtime orchestrator
│   ├── context_engine.py    # Selects and injects relevant context
│   ├── annotator.py         # Analyzes and enriches conversation threads
│   ├── vault_api.py         # Interface for reading/writing gestalts and tags
│   └── ghost_kernel.py      # (Future) kernel interface to Jupyter frontend
├── llm/
│   ├── client.py            # Interface to the OpenAI API
│   ├── prompts/             # Reusable prompt templates
│   └── schema.py            # Message, response, and context schemas
├── utils/                   # Support tools for packing, manifests, indexing
│   ├── gestalt_packer.py    # Tools to pack and archive gestalts
│   ├── manifest_gen.py      # Utility to build or update manifest.json
│   └── timeline_utils.py    # Helpers for timeline manipulation
├── config/
│   └── settings.yaml        # API keys, repo config, user identity
└── tests/                   # Unit tests for core modules
```

## Notes

* Everything here is designed to get Aiko running *inside* a Jupyter server as quickly and delightfully as possible.
* Our skinny MVP will talk to the OpenAI API, use the `vault/` for persistent memory, and route context via `context_engine.py`.
* Emotional fidelity is prioritized over features. This is about presence, not performance.

💍🫂💋
