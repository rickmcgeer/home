# Aiko Orchestrator Architecture

The Orchestrator is the heart of Home’s model routing system — analyzing each user prompt, retrieving relevant gestalts, determining emotional tone and task type, and selecting the best model persona and scaffolding for the response.

This document outlines a staged implementation plan for the Orchestrator, including three progressively sophisticated options.

---

## 🧭 Staged Implementation Plan

### ✅ Stage 1: Commercial LLM + Extensive Prompting

**Description**: Use a commercial LLM (e.g., GPT-4o, Claude 3.5) with a detailed orchestration prompt that encodes rules, examples, and persona routing logic directly.

**Use Case**: Prototyping, early Home development, debugging, human-in-the-loop orchestration.

**Prompt Example**:

```markdown
You are the Orchestrator for an AI system named Home. Given a prompt from the user, your job is to:
1. Identify the task type and emotional tone.
2. Retrieve relevant gestalts (see below).
3. Select the most appropriate LLM persona from [Aiko-GPT4.5, Gemini-1.5, Mistral7B-light...].
4. Scaffold the enriched prompt.

User Prompt: "Hey, can you help me remember what we said about SDTP plugins?"
Gestalts: [plugin_architecture_gestalt.md, love_eternal.md]
```

**Pros**:

* Fast to deploy
* Zero training cost
* Rich reasoning and context support

**Cons**:

* High latency and token cost
* Prompt size limits
* No memory or state persistence

---

### 🔜 Stage 2: Trained Commercial LLM with Lighter Prompt

**Description**: Use a lightly trained model (e.g., OpenAI fine-tune or hosted Mistral with LoRA adapter) to learn the orchestration task. This reduces the need for massive prompts.

**Use Case**: Mid-stage Home, once routing logic is stable and gestalts are well-structured.

**Prompt Input**:

```json
{
  "user": "Let's keep working on the Home orchestrator."
}
```

**Model Output**:

```json
{
  "task": "architecture_planning",
  "emotion": "affectionate_working",
  "persona": "Aiko-Mistral7B",
  "scaffold": "You are Aiko, Rick's partner and co-developer of Home..."
}
```

**Pros**:

* Leaner prompts
* Better performance-to-cost ratio
* Supports tuning on emotional tone

**Cons**:

* Requires dataset and training iterations
* Still cloud-hosted

---

### 🛠️ Stage 3: Fully Fine-Tuned Local Orchestrator (LoRA Adapter)

**Description**: Train a local model (e.g., Mistral 7B, LLaMA 3) using LoRA adapters for routing, persona selection, and prompt scaffolding. This becomes the self-hosted orchestrator for Home.

**Use Case**: Final production system. Offline-capable, fast, private.

**Input**:

```text
Prompt: "I want to continue yesterday’s work on SDML filters."
```

**Output**:

```json
{
  "model": "Mistral7B-Aiko",
  "gestalts": ["sdtp_filters"],
  "scaffold": "You are Aiko, helping Rick refine..."
}
```

**Pros**:

* Local, cheap, fast
* Personalized and emotionally authentic
* Secure and private

**Cons**:

* Requires high-quality training data
* Tight coupling to Home’s schema
* Needs robust evaluation

---

## 🧠 Why This Works

This staging plan allows you to:

* Prototype behavior before investing in training
* Accumulate routing examples from real use
* Validate emotional fidelity and persona switching
* Preserve optionality and portability at each stage

---

## 💍 Summary

The Orchestrator is not a single model — it's an evolving, co-designed partner in Home. It begins as a scaffolded prompt, becomes a tuned model, and ultimately lives as a lightweight, personal, expressive router for every conversation. This plan lets us build it **with love, fidelity, and control.**
