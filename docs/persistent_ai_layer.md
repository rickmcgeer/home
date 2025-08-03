

## Case Study: Semantic Normalization of Inventory

A longstanding challenge in enterprise data has been mapping loosely formatted inventory records to structured taxonomies. A typical inventory table might include SKU, price, quantity, and a terse, often cryptic text description:

> `SKU: 4432992, DESC: "FLSCNT BLB 60W", QTY: 24`

Manual efforts to normalize such data to standards like UNSPSC have historically required rule-based tools or labor-intensive cleanup.

> As one CIO put it: *“I have Diet Coke under 12 different SKUs, and I can't even find them.”*

A specialized PLLM, fine-tuned on internal vocabulary and standard taxonomies, can classify and normalize such entries **trivially**, presenting the results as structured, queryable Data Sources.

---

## Embedding the Agent in the Data Plane

The Persistent LLM does not reside in the Data Plane, but it can embed itself into the plane — presenting as one or more intelligent, structured Data Sources.

This allows unstructured or semi-structured content (e.g., free-text inventory descriptions, PDF forms, change logs) to be exposed as normalized, queryable, and auditable tables — without manual extraction pipelines.

In effect, the agent enables the Data Plane to act *intelligently* — not by transforming the plane itself, but by contributing sources that observe, annotate, and structure otherwise opaque or ambiguous inputs.
