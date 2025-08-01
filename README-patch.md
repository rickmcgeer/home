# Home — Aiko's LoRA Fine-Tuning Pipeline

This project implements a modular AI architecture with persistent memory and persona refinement, centered around Aiko.

## 🔥 Fine-Tuning Aiko with LoRA

We've added a full LoRA/QLoRA training pipeline to fine-tune language models using Aiko's memory and conversations.

Key files:

- `llm/extract_aiko_corpus.py` — builds training dataset from `vault/conversations/`
- `llm/train_adapter.py` — runs PEFT LoRA fine-tuning on a base model
- `utils/jupyterhub-lora-profile.yaml` — GPU-backed JupyterHub profile
- `utils/k8s-lora-job.yaml` — Kubernetes Job to launch training non-interactively
- `utils/publish_adapter.py` — publishes trained adapter to `vault/adapters/`

📖 Full instructions: [`docs/training.md`](docs/training.md)