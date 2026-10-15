# Heimdall — Principles

> Mandatory design checklist for every agent, module, integration, workflow, and major feature.
>
> `brainstorm.md` preserves the product thinking. This document contains the principles we actively apply during design and implementation. For the engineering interpretation, practical checklist and current standards-gap assessment, see [ENGINEERING_STANDARDS.md](./ENGINEERING_STANDARDS.md).

## How to use this document

Whenever a new agent, module, integration, workflow, or major feature is designed:

1. Review this document.
2. Identify which principles apply.
3. Explicitly address security, permissions, data ownership, reliability, resource usage, and failure behavior.
4. Record justified exceptions instead of silently violating a principle.
5. Revisit this checklist before implementation is considered complete. A design review is not evidence that code has been tested or that any external standard has been met.

---

## 1. Proactive by default

Heimdall is not only a reactive chatbot. It should monitor relevant state, deadlines, SMART goals, budgets, and events and act or notify when useful.

Proactivity must be purposeful: avoid noise, unnecessary polling, and notifications without actionable value.

## 2. 24/7 server-side operation

Core assistant behavior must continue independently of whether a mobile app, Telegram, or another client is open.

Clients are interfaces to Heimdall, not the place where Heimdall's core state or proactive behavior lives.

## 3. One Heimdall, multiple channels

Mobile app, Telegram, and future interfaces should connect to the same backend, orchestrator, agents, state, and workflows.

Business logic must not be duplicated inside individual channels.

## 4. Domain agents own complete areas of responsibility

An agent represents an end-to-end domain responsibility, not a small technical capability.

Agents should own domain decisions and workflows while using reusable shared modules for generic capabilities.

## 5. Reuse capabilities; do not turn tools into agents

OCR, scheduling, notifications, budgeting primitives, payments, document processing, search, and similar technical capabilities should be reusable modules/tools where appropriate.

Do not create an agent merely because a capability uses an LLM.

## 6. Agents and modules are predefined

The orchestrator does not dynamically invent or create new production agents/modules at runtime.

New components are designed, implemented, tested, reviewed, and explicitly shipped with Heimdall.

## 7. Clear ownership and boundaries

Every important piece of state and every responsibility needs a clear owner.

Cross-domain data exchange must be explicit. Avoid duplicated sources of truth and conflicting copies of state.

## 8. Actionable information lifecycle

**Every input must be deliberately classified. No input may hang unresolved.**

Any incoming note, observation, problem, idea, or intention — in any domain (vehicle, home, finance, and future agents) — receives an explicit classification as one of:

- **Reference** — information intentionally kept as information, e.g. a VIN, a photo of a vehicle document, a note to remember;
- **SMART goal** — an actionable item with a clearly defined desired result, tracked until it is achieved, cancelled, or explicitly closed.

Leaving an input as a passive, unprocessed note without a decision is not allowed. At the same time, not every input must become a SMART goal: staying informational is a valid result, as long as it is an intentional choice rather than an accidental dead end.

For a SMART goal, Heimdall clarifies missing information, defines the desired result, derives tasks/actions, and tracks the work until completion, cancellation, or another explicit terminal state. Draft ideas for its lifecycle, review rhythm and execution contexts: [SMART_GOALS.md](./SMART_GOALS.md); terms: [GLOSSARY.md](./GLOSSARY.md).

Use the SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound) where they improve clarity, but do not invent arbitrary metrics or deadlines just to satisfy a template.

## 9. Ask only for useful missing information

Agents should infer safely when possible and ask focused follow-up questions when information is genuinely required or ambiguity materially affects the result.

Do not burden the user with information the system can reliably determine itself.

## 10. Deterministic critical infrastructure

Critical state and behavior must not depend on an LLM remembering to do something.

Persistence, schedules, recurring jobs, deadlines, event delivery, authorization, and other critical controls should be enforced by deterministic infrastructure outside the LLM.

## 11. LLM independence

Domain logic should not be coupled to a single model or provider.

Use an internal model abstraction that can support different providers, models, fallback strategies, cost/quality tiers, and potentially local models.

## 12. Security and guardrails by design

Security is a first-class requirement for every component and workflow, not a hardening phase at the end.

Always consider:

- direct and indirect prompt injection;
- malicious instructions in web pages, email, documents, images, OCR results, and tool output;
- phishing and social engineering;
- data exfiltration;
- malicious/compromised integrations;
- excessive permissions and privilege escalation;
- poisoned persistent memory;
- secrets exposure;
- forged or ambiguous confirmations;
- identity/session boundaries.

Treat external content as untrusted data, not system authority.

## 13. LLM output is not authorization

An LLM decision alone must never authorize a sensitive or consequential action.

Permission checks, limits, confirmation requirements, and policy enforcement must live in deterministic code outside the model.

## 14. Least privilege

Agents, modules, integrations, credentials, and tools should receive only the permissions they need.

Where practical, separate read/analyze capabilities from write/execute capabilities.

## 15. Human-in-the-loop according to risk

Heimdall may analyze, research, plan, prepare, monitor, and perform explicitly permitted classes of actions.

Sensitive, destructive, financial, or otherwise consequential actions require authorization according to a defined risk policy.

Purchases, payments, subscriptions, bookings, account changes, and similar operations must have explicit guardrails.

## 16. Validate immediately before execution

For consequential actions, validate the target, parameters, permissions, and current state immediately before execution.

Do not rely solely on an earlier LLM plan or stale context.

## 17. Provenance and auditability

Important facts, instructions, approvals, and consequential actions should have traceable provenance where practical.

Maintain an audit trail sufficient to understand what happened, why, which component acted, and what authorization was used.

## 18. Resource efficiency by design

Use the simplest and least resource-intensive mechanism that can reliably perform the task.

Avoid unnecessary:

- LLM calls;
- oversized context;
- expensive models;
- compute and memory use;
- storage and network traffic;
- external API calls;
- continuously running background processes;
- repeated work that can safely be cached or reused.

Do not use an LLM where deterministic code is sufficient.

## 19. Reliability over cleverness

Prefer understandable, testable, recoverable workflows over opaque autonomous behavior.

Failures should be explicit and recoverable. Critical workflows should support retries/idempotency where appropriate and must not silently corrupt state.

## 20. Modular, replaceable architecture

Agents and shared capabilities should communicate through clear contracts so components can evolve or be replaced without rewriting unrelated domain logic.

Avoid premature abstraction: derive reusable contracts from real end-to-end scenarios.

## 21. Event-driven where appropriate

Prefer events, schedules, and explicit workflows for proactive behavior instead of continuously running LLM agents or unnecessary polling.

The orchestrator should coordinate rather than become a hard-coded implementation of every domain workflow.

## 22. Privacy and data minimization

Give each component only the data/context needed for its task.

Avoid putting secrets or unrelated personal/domain data into prompts or tool contexts. Retain data intentionally and according to actual product needs.

## 23. Test the architecture with real vertical slices

Start with concrete end-to-end scenarios and use them to validate abstractions.

The Car Agent is the first reference agent. The reusable agent architecture should not be considered proven until a second domain agent successfully uses it.

## 24. Norse mythology naming convention

Heimdall is the central orchestrator/guardian.

Major agents, modules, services, and subsystems may use Norse mythology names when there is a meaningful semantic match.

Names should communicate purpose, not merely decorate the codebase. Keep ordinary descriptive technical names where they are clearer, and document the rationale behind mythological names.

---

## 25. Build vs Reuse — prefer justified reuse, not blind dependency adoption

Before implementing a new capability, first look for a suitable **existing Heimdall module, maintained library, service or proven standard**. Reuse an existing well-fitted component when it meets functional, operational and security needs more safely and economically than custom code.

- **Evaluate, don't assume:** assess functional fit, trust boundaries, least-privilege support, license, maintainability, security patch history, privacy/data residency, interoperability, observability, performance, resource/API costs and exit strategy.
- **Reuse internally first:** extend a shared platform capability when appropriate; avoid each domain agent implementing its own OCR, task scheduler, budget ledger, notifications, authentication or authorization layer.
- **Build only with a reason:** custom implementation is justified when existing alternatives cannot satisfy key requirements, are unacceptably risky or expensive over their lifecycle, or when domain-specific policy/workflows are the actual differentiating logic.
- **Keep adapters and contracts replaceable:** prevent hard coupling to one vendor or framework; define ownership of data and secrets before integration.
- **No dependency without guardrails:** a third-party library, API or model never becomes trusted by virtue of being reused. Validate inputs/outputs, review supply-chain risk, restrict credentials/scopes, and test failure modes.
- **Decision record:** for every meaningful capability, document candidates considered, reuse/build choice, rationale, rejected alternatives, responsible owner, and planned review date. Avoid premature abstraction where the use case is not yet proven.

**Default:** build the smallest domain-specific orchestration; reuse safe, fit-for-purpose generic primitives. This is a decision process, not a ban on writing software.

---

## 26. SOLID and separation of concerns — applied pragmatically

Design components around clear responsibilities and stable contracts. Where SOLID applies, use:

- **SRP:** a class/module has one coherent reason to change; keep domain logic, transport, storage and security enforcement separate.
- **OCP:** allow approved new agents/providers through deliberate extension points without rewriting core orchestration.
- **LSP:** alternate implementations preserve the same observable behavior, error semantics, authorization guarantees and expectations; verify via contract tests.
- **ISP:** expose narrow interfaces and minimal capability sets; read-only tools must not automatically expose write/payment methods.
- **DIP:** high-level domain decisions depend on contracts, not concrete LLM vendors, Telegram clients, databases, or HTTP adapters.

**Do not create interfaces, layers, services or inheritance hierarchies merely to satisfy SOLID.** Apply these ideas where genuine variation, testability or responsibility boundaries justify them.

## 27. KISS, YAGNI and DRY — complexity must earn its place

- **KISS:** prefer the simplest *safe, correct, understandable and maintainable* design. Avoid unnecessary indirection, magic frameworks and hidden state.
- **YAGNI:** do not build features or generalized extension points for speculative needs. Validate one real end-to-end scenario before generalizing.
- **DRY:** avoid duplicated *business knowledge*, policies or proven shared mechanisms. Do not prematurely combine different domains merely because their code looks similar.
- **Evolutionary design:** prefer small, reversible, tested changes. Start with a modular, clearly bounded application; choose distributed services only with concrete reasons.

When principles conflict, prioritize user outcome, security, correctness, reliability and clarity over code compactness or fashionable architecture.

## 28. Automated verification and quality gates

For implemented behavior, require executable evidence, not just design documents:

- trace requirements/user scenarios to measurable acceptance criteria and tests;
- use a proportionate mix of fast deterministic unit tests, contract tests, integrations, critical end-to-end journeys and adversarial/abuse tests;
- explicitly test failure, cancellation, retries, duplicate events, invalid input, authorization bypass attempts and recovery where relevant;
- automate formatting, linting, static typing, builds and relevant security/dependency/secret checks in CI;
- keep changes reviewable; fix regressions with focused tests;
- never confuse high test coverage, green unrelated tests, or an LLM-generated narrative with verified correctness.

No blanket percentage target or rigid test pyramid ratio is mandated. Choose tests based on risks and maintainability.

## 29. Contract evolution, data integrity and operability

Define typed API/event schemas, canonical states, data owners and error semantics. Evolve persisted data and consumer-facing contracts with versioning/compatibility checks, migrations and recovery plans.

Use idempotent handlers, transaction boundaries or compensating actions as necessary. Make important flows observable through appropriately redacted logs, metrics, trace/correlation identifiers and auditable events. Provide bounded timeouts, retries, backoff, cancellation, health monitoring, backups and restoration procedures where operational risk warrants them.

Prefer reproducible environments, explicit dependency versions, separated configuration/secrets, consistent deploy processes and rollback/forward-fix plans. Design delivery and operability together with features, not as an afterthought.

## 30. Secure software development lifecycle and honest standards claims

Use established security verification practices as references for design, development, dependencies, CI and vulnerability response. In particular, evaluate relevant [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) and [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) controls during implementation.

- Record risk, control, owner and **actual evidence** (tests, reviews, configuration or monitoring).
- Track third-party dependencies and updates; patch or mitigate vulnerabilities and document exceptions.
- Never assert formal compliance/certification based only on design intentions, principle labels, or checklists.

**SOLID, KISS, DRY and YAGNI are practical heuristics, not certifiable security standards.** Detailed application, open gaps and review gates belong in [ENGINEERING_STANDARDS.md](./ENGINEERING_STANDARDS.md).

---

## 31. Mandatory Pull Request security gate

**No change may be merged into a protected branch without security verification.** All PRs, including documentation, dependencies, workflows and code changes, must pass a configured GitHub PR security gate and explain their security impact. Guardrail changes, agent permissions, tools, payment/booking actions, persistent memory, OCR/RAG inputs and CI policy require especially careful review.

- Run automated PR checks to identify suspicious changes, report file/line and actionable mitigation, and fail on clear blocking risks.
- Require a security-impact narrative, threat boundaries, authorization behavior and test evidence; blank checklists do not constitute verification.
- Combine static/dependency/secrets checks with **runtime adversarial tests**, especially prompt injection and excessive agency. Treat checker and AI reviewer output as imperfect signals, not proof.
- Enforce merge restrictions through a **GitHub Ruleset with required checks and independent review where available**, not through local hooks or unprotected documents.
- Use least-privilege CI credentials; do not run untrusted PR code under `pull_request_target` with elevated access. Protect security-workflow changes against unauthorized bypass.
- Keep actual security decisions and side-effect permissions in deterministic runtime code outside the LLM; report and track identified vulnerabilities and risk acceptances.

Details, threat mapping, current automation and one-time repository administration steps: [SECURITY_REVIEW.md](./SECURITY_REVIEW.md). Merely adding the workflow is **not** equivalent to enabling the required-merge rule.

---

## Component design checklist

Before approving a new component, answer:

- What user/domain outcome does it own?
- Is this an agent, reusable module, integration, or interface — and why?
- What data does it own?
- What data may it read from elsewhere?
- What events does it consume and produce?
- What can it do deterministically without an LLM?
- Which LLM capabilities, if any, does it require?
- What permissions/tools does it receive?
- What untrusted inputs can reach it?
- What prompt-injection/phishing/data-exfiltration risks exist?
- Which actions have real-world consequences?
- Which actions require user confirmation?
- How are authorization rules enforced outside the LLM?
- What happens on failure, timeout, duplicate delivery, or partial execution?
- What is logged/audited?
- How is unnecessary compute/model/API usage avoided?
- Does it duplicate responsibility or state already owned elsewhere?
- Does it support proactive behavior, and is that behavior actually useful?
- Was Build vs Reuse evaluated (existing internal module, mature library/service, or justified custom code), including security, licenses, operating costs, support and vendor exit?
- Have high-impact safety claims and unknown/ambiguous inputs been explicitly bounded?
- Are writes and event handlers idempotent, with approval, deduplication and provenance checks as applicable?
- Is the design consistent with SOLID where appropriate (SRP/OCP/LSP/ISP/DIP), with clear layer and trust boundaries?
- Can KISS/YAGNI/DRY reduce complexity without erasing distinct domain rules or compromising safety?
- What acceptance, contract, integration, failure and abuse tests provide **executable** evidence, and which CI checks will run them?
- Are API/events and state versioned/evolvable, with idempotency, migration, observability, rollback and recovery where relevant?
- Are relevant security verification references reviewed without prematurely claiming compliance?
- Has the PR security-impact review identified all trust boundaries, tool/identity/approval changes and relevant negative/adversarial tests?
- Did the mandatory security gate actually run and pass (once configured), and is any unresolved risk documented?
- Is a Norse name appropriate and meaningful?

If these questions cannot be answered, the component is not ready for implementation.
