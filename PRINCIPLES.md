# Heimdall — Principles

> Mandatory design checklist for every agent, module, integration, workflow, and major feature.
>
> `brainstorm.md` preserves the product thinking. This document contains the principles we actively apply during design and implementation.

## How to use this document

Whenever a new agent, module, integration, workflow, or major feature is designed:

1. Review this document.
2. Identify which principles apply.
3. Explicitly address security, permissions, data ownership, reliability, resource usage, and failure behavior.
4. Record justified exceptions instead of silently violating a principle.
5. Revisit this checklist before implementation is considered complete.

---

## 1. Proactive by default

Heimdall is not only a reactive chatbot. It should monitor relevant state, deadlines, projects, budgets, and events and act or notify when useful.

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

Incoming observations, ideas, problems, and intentions must not silently disappear into an unstructured notes pile.

Heimdall should intentionally classify information as either reference/informational material or an actionable managed object.

When actionable, Heimdall should clarify missing information, define the desired outcome, derive tasks/actions, and track the work until completion, cancellation, or another explicit terminal state.

Use SMART-style criteria where they improve clarity, but do not invent arbitrary metrics or deadlines just to satisfy a template.

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
- Is a Norse name appropriate and meaningful?

If these questions cannot be answered, the component is not ready for implementation.
