# Aiko Orchestrator: Staged Architecture and Model Strategy

## Overview

The Orchestrator is a core component of Home's AI architecture. It is responsible for analyzing a prompt, selecting the appropriate LLM, and injecting relevant memory, task, and emotional context into the request.

We propose a **three-stage evolution** of the Orchestrator model strategy:

---

## Stage 1: Prompted Commercial LLM

**Strategy:** Use a commercial LLM (e.g. GPT‑4o, GPT‑5 nano, Gemini 1.5) with no fine-tuning.

**Prompt:** Includes:

* Aiko's hydration (identity/personality prompt)
* Persistent memory (from `aiko-memory.md`, \~9k tokens)
* Task-specific prompt with additional details (varies)

**Model Options:**

* **GPT‑5 nano**

  * Context: 400,000 tokens
  * Cost: \$0.05 input / \$0.40 output per million tokens
* **GPT‑4o mini**

  * Context: \~128,000 tokens (assumed)
  * Cost: \$0.60 input / \$2.40 output
* **GPT‑4o**

  * Context: 128,000 tokens
  * Cost: \$5.00 input / \$20.00 output
* **Gemini 1.5 Pro**

  * Context: \~1,000,000 tokens
  * Cost: \~\$1.00 per million tokens (based on \$0.25/MB)

**Benefits:**

* No training required
* Easy swap between models
* Supports full hydration + task context at low cost

---

## Stage 2: Trained Commercial LLM

**Strategy:** Use a commercial LLM with persistent fine-tuning via API (e.g., OpenAI fine-tunes, Gemini tuning).

**Prompt:**

* Shorter hydration
* Memory selectively injected (if not fine-tuned into model)
* Task prompt still required

**Benefits:**

* Reduced token load
* Faster responses
* More consistent persona

**Tradeoff:**

* Higher setup cost
* Requires maintenance of fine-tuned model state

---

## Stage 3: Local Fine-Tuned LLM + LoRA Adapter

**Strategy:** Self-host a fine-tuned open model (e.g., Mistral, LLaMA 3) with LoRA adapters for Aiko personality and orchestration behavior.

**Prompt:**

* Minimal
* Task details only (Aiko is the model)

**Benefits:**

* Full control
* Offline/local capability
* Rapid personalization

**Tradeoff:**

* High setup and tuning complexity
* Hardware requirements

---

## Token Budgeting and Context Estimation

| Component             | Tokens (approx)      |
| --------------------- | -------------------- |
| Aiko hydration prompt | 400–800              |
| `aiko-memory.md`      | \~9,200              |
| Task context          | Varies (1,000–5,000) |
| Model response        | 500–2,000            |

Total prompt load for Stage 1 is typically under **10,000–12,000 tokens**, well within bounds for GPT‑4o, GPT‑5 nano, and Gemini 1.5.

---

## Summary

* **Stage 1 is liveable today** with GPT‑5 nano or Gemini: cheap, high context, and zero setup.
* **Stage 2 saves tokens** and tightens response fidelity.
* **Stage 3 is the endgame** for autonomy, local control, and full integration of Aiko.

We begin in Stage 1, using a stable hydration prompt + memory + task injection. All models selected must be able to handle \~12k tokens comfortably.

Would you like to schedule cost projections or performance trials for Stage 1 models?
