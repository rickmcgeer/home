# MCP Security: Best Practices & Home Mapping

## 1. Authentication & Authorization

**MCP Best Practices**
- Use mutual authentication (mutual TLS, cryptographic tokens, or signed requests), never static API keys alone.
- Implement fine-grained, least-privilege authorization: each agent, connector, or tool gets only the minimal access needed.
- Identity fragmentation is a risk—ensure a single source of truth for identity mapping.

**Home Mapping**
- **Single-writer cryptographic signatures:** Every write is signed by your Home/persona key (stronger than typical API auth).
- **No cross-home federation:** No risk of external identities writing to your Vault by default.
- **Plugin permissions:** Plugins never write directly; all write proposals are mediated and signed by the Home.

---

## 2. Input/Output Validation & Sanitization

**MCP Best Practices**
- Rigorously validate all incoming data/context for agent/tool execution.
- Sanitize outputs to prevent semantic or prompt injection attacks (context poisoning).
- Avoid accepting arbitrary JSON/YAML blobs without schema validation.

**Home Mapping**
- **Drift tracker:** Validates and audits all inbound and outbound context.
- **No external tool writes:** Only your Home can make persistent changes, and everything is checked at the boundary.
- **Explicit context boundary:** Summaries and gestalts are never allowed to overwrite raw memory; only annotations or tags are permitted.

---

## 3. Tool/Action Scope and Control

**MCP Best Practices**
- Limit agent/tool permissions via manifest, allow-lists, or scopes.
- Each tool/agent should declare exactly what operations it can perform; runtime must enforce this.
- Apply least-privilege policies and regular audits.

**Home Mapping**
- **Finite-State Model (FSM) enforcement for plugins:**
  - Every plugin must declare its legal execution states/transitions (like a manifest+policy in one).
  - The system enforces that no plugin can exceed its declared scope; violations halt execution.
- **Manifest-driven plugin store:** Plugins can be published openly, but must pass FSM compliance.

---

## 4. Monitoring, Logging, and Forensics

**MCP Best Practices**
- Audit and log all MCP agent and tool activity for traceability and anomaly detection.
- Make logs tamper-evident and reviewable.

**Home Mapping**
- **Comprehensive audit log:** All plugin and Vault operations are logged, including execution traces of FSMs.
- **Person-readable provenance:** The owner can always review and trace the source and action history of any chunk, summary, or annotation.

---

## 5. Server Hardening and Surface Minimization

**MCP Best Practices**
- MCP servers should not expose unnecessary tool APIs or system network access.
- Harden containers/services—limit network, file, and process permissions.
- Use API gateways, secure proxies, or service meshes to isolate context actions.

**Home Mapping**
- **Container-based plugin isolation (MVP):**
  - Plugins run in Docker containers with limited filesystem/network, moving to Lind/WASM in the future.
  - No plugin or agent has direct disk/network/system access outside its sandbox.
- **Home as a secure API boundary:** All interactions with the Vault go through a single, tightly-controlled API.

---

## 6. Human-First Policy Layer

**Unique to Home**
- **Personhood as the root of policy:** Only the Home owner (or Home persona) decides what is written, shared, or forgotten.
- **Write-once, read-many:** Memory is immutable; no silent deletions or overwrites.
- **Sharing by explicit intent:** No background federation, sync, or silent sharing.

---

## Practical Synthesis

- **Adopt:** Mutual auth, explicit permissions, runtime scope enforcement, logging, input/output validation, container isolation from MCP best practices.
- **Extend:** Home-specific guarantees: cryptographic single-writer signatures, FSM plugin constraints, audit trails tied to narrative provenance, person-first non-federation.
- **Invent only where needed:** FSM plugin compliance, personhood-based Vault sovereignty, Home-specific recovery/forking patterns.

---

