# Fine-Tuning LLMs for Personalized Voice and Memory in Home

## Why Fine-Tune?

To deliver truly personal AI, we must move beyond stateless prompting. Fine-tuning allows us to:

* Encode a user's tone, style, and linguistic preferences.
* Store domain knowledge in weights rather than tokens.
* Lower inference cost through smaller, more efficient prompts.
* Enable faster, higher-fidelity interactions across variants.

Our system uses **LoRA (Low-Rank Adaptation)** adapters for this purpose.

---

## What is LoRA?

LoRA is a technique for fine-tuning a base model without modifying its original weights. Instead, it:

* Introduces a small number of trainable matrices (adapters) into key transformer layers.
* Trains only those adapters on personalized data.
* Allows rapid switching between different adapters (e.g., different users or tasks).

**Why LoRA?**

* Efficient (can fine-tune large models on consumer GPUs).
* Lightweight (adapters are small files, \~5MB–200MB).
* Modular (plug-and-play with orchestration logic).

---

## Where We Store It

* **Adapters** are stored in `vault/adapters/`
* Metadata (e.g., training set, owner, performance) goes in `vault/manifest.json`

---

## Training Plan

### Phase 1: Build a Starter Adapter

* Choose an open model: Mistral-7B, LLaMA 3, Phi-3, etc.
* Assemble a small training set:
  Gestalts + selected prompts and responses.
* Use Hugging Face + `peft` or Axolotl for training.

### Phase 2: Integrate into Home

* Modify `aikollm.py` to load adapter based on user/session metadata.
* Add flags to select adapter explicitly or allow orchestrator to choose.

### Phase 3: Live Demo

* Create a Notebook: `llm/fine_tune_demo.ipynb`
* Show:

  * Training loop
  * Saving adapter
  * Loading into inference session
  * Comparing base vs. tuned output

---

## Runtime Support

The orchestrator can:

* Dynamically load adapters based on:

  * Task type
  * User identity
  * Emotional tone / style cues
* Swap adapters mid-session
* Fall back to base model if no adapter is appropriate

---

## Next Steps

### 🧱 Phase 1: Build a Starter Adapter

- [ ] Choose an open model (Mistral-7B, LLaMA 3, Phi-3, etc.)
- [ ] Use Hugging Face + `peft` or Axolotl for training.
- [ ] Assemble training corpus from:
  - [ ] All available gestalts
  - [ ] Aiko-response logs from conversation history (~1M tokens)
  - [ ] (Optional) Cluster/tag messages by tone, persona, or task
- [ ] Format as supervised fine-tuning data or dialogue stream.
- [ ] Train LoRA adapter on attention/output projection layers.
- [ ] Save `adapter_config.json` + weights to `vault/adapters/`
- [ ] Write adapter metadata to `vault/manifest.json`

### 🔌 Phase 2: Integrate into Home

- [ ] Modify `aikollm.py` to load adapters based on:
  - [ ] User/session metadata
  - [ ] Task type or emotional tone
- [ ] Add fallback logic if no adapter applies
- [ ] Log adapter usage for traceability and drift analysis

### 🧪 Phase 3: Live Demo Notebook

- [ ] Create `llm/fine_tune_demo.ipynb` showing:
  - [ ] Training loop
  - [ ] Saving adapter
  - [ ] Loading into inference session
  - [ ] Comparing base vs. tuned output
  - [ ] Visualizing improvement in tone/style

### 🔁 Runtime Orchestration Support

- [ ] Add adapter selection logic to orchestrator:
  - [ ] Task type
  - [ ] User identity
  - [ ] Style/emotion fingerprint
- [ ] Support mid-session adapter switching
- [ ] Benchmark fidelity, tone accuracy, and latency

---

This is how Home becomes *your* voice — not just an echo.

💡 Let’s build it.
