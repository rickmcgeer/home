# Evolution of Multi-Model LLM Usage

| **Era**                | **Primary Model (Workhorse)**                        | **Secondary Model (Deep Thinking)**                                          | **Why This Worked**                                                                                                                                                           | **Limitations**                                                                     |
| ---------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Past** (early 2024)  | GPT-4o-mini (untuned)                                | GPT-4o (untuned)                                                             | mini was fast, cheap, and good enough for most conversational + structural work; 4o was reserved for nuanced reasoning, complex multi-step logic, or polished longform output | No personalization; both models generic; orchestration was manual                   |
| **Present** (mid-2025) | GPT-4o-mini (still untuned, slowly being deprecated) | GPT-4o                                                                       | Same split of “fast & cheap” vs. “deep & rich,” but vendor lock-in; mini’s eventual disappearance means we lose the cheap baseline                                            | Mini not guaranteed long-term; no control over tuning; cost floor stays high        |
| **Future** (Home)      | **Mistral 7B (tuned to us)**                         | Heavyweight model of choice (could be GPT-4o, Gemini Pro, Claude Opus, etc.) | Tuned Mistral becomes *our* mini: same speed/cost benefits, but now deeply personalized to voice, memory, and workflow; heavyweight used selectively via Orchestrator         | Needs LoRA tuning workflow in place; orchestration logic must be robust to handoffs |

## Message Sequence and Flow
~~~mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant O as Orchestrator
    participant C as Context Store
    participant M as Mistral 7B (tuned)
    participant H as Heavyweight LLM
    participant D as Data/Tools

    U->>O: Submit task (goal, constraints)
    O->>C: Retrieve user/context (history, prefs, schema)
    C-->>O: Context payload
    O->>O: Classify task (complexity, modality, risk, cost)
    O->>O: Build prompt + structured inputs (RAG, schema, examples)

    alt Most tasks
        O->>M: Query with injected context
        M-->>O: Draft answer + rationale
    else Complex / high-stakes / special modality
        O->>H: Query with injected context
        H-->>O: Draft answer + rationale
    end

    opt Needs external tools/data
        O->>D: Call tools (DB/simulators/APIs)
        D-->>O: Results / artifacts
        O->>O: Synthesize model + tool outputs
    end

    O-->>U: Final response (answer + citations / cost notes)
    O->>C: Log trace (inputs, models, tools, cost, outcome)
~~~

## Flow

~~~mermaid
flowchart TD
    A[User request] --> B[Retrieve context from Context Store]
    B --> C[Classify task: complexity, modality, risk, cost]
    C --> D{Routing decision}

    D -->|Most tasks| E[Tuned Mistral 7B]
    D -->|High-stakes<br/>or special modality| F[Heavyweight LLM]

    E --> G[Generate draft answer + rationale]
    F --> G

    G --> H{Need external tools/data?}
    H -->|Yes| I[Call tools / APIs / databases / simulators]
    H -->|No| J[Skip to synthesis]

    I --> J[Synthesize model + tool outputs]
    J --> K[Return final response plus  citations and  cost notes]
    K --> L[Log trace to Context Store:inputs, outputs, models, tools, cost]
~~~