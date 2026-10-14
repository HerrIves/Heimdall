# Heimdall

**Heimdall** is a modular, proactive personal assistant platform.

Heimdall is the central orchestrator: one brain, multiple channels and specialized domain agents. The name refers to Heimdall, the watchman of Norse mythology, reflecting the system's goal of observing relevant events, noticing them early, and proactively helping the user.

## Project status

**Current phase:** Phase 3 — selection and formalization of the first MVP vertical slice (Hrimfaxi).

**Current work and the next concrete step are tracked in [PROGRESS.md](./PROGRESS.md).** The brainstorming and requirements audit are complete. The first vehicle domain agent has now been named **Hrimfaxi**, with an initial specification and ten user scenarios. **Current phase: choose and formalize the first MVP vertical slice (Phase 3).** The proposed candidates are fault reporting (UC-01) and invoice ingestion (UC-03); the final selection is still open.

## Start here

1. **[PROGRESS.md](./PROGRESS.md)** — current stage, completed work, blockers, and the exact next action. Read this first when continuing work.
2. **[REQUIREMENTS.md](./REQUIREMENTS.md)** — product behaviors, scoped/candidate ideas, open decisions and mapping of all 18 brainstorm sections.
3. **[PRINCIPLES.md](./PRINCIPLES.md)** — mandatory rules and the component-review checklist.
4. **[ENGINEERING_STANDARDS.md](./ENGINEERING_STANDARDS.md)** — SOLID, KISS, DRY, YAGNI, quality gates and review against engineering/security references.
5. **[PLAN.md](./PLAN.md)** — the full roadmap, milestones and review gates.
6. **[CAR_AGENT.md](./CAR_AGENT.md)** — initial Hrimfaxi vehicle-agent behavioral specification and domain boundaries.
7. **[HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md)** — catalog of ten proposed user scenarios and potential MVP slices.
8. **[HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md)** — static review of all 10 cases, blockers, safety checks and Build vs Reuse decisions.
9. **[brainstorm.md](./brainstorm.md)** — original ideas and their rationale; preserved for historical context.
10. **README.md** — this document: repository introduction and documentation map.

The design must trace product requirements back to the brainstorm, but avoid duplicating them in the plan or README. A root-level `AGENTS.md` does **not** yet exist; if created later, it should contain instructions for repository coding assistants, not repeat the product requirements or list speculative agents as implemented.

## Core concept

- Heimdall is the orchestrator, not a monolithic agent.
- Domain agents own end-to-end workflows and domain knowledge.
- Shared modules provide reusable capabilities such as tasks, scheduling, documents/OCR, budgets, notifications, and approvals.
- Multiple interfaces can use the same backend: a dedicated app, Telegram, voice, and potentially other channels.
- Notes and observations should not simply disappear into storage. Heimdall determines whether something is reference information or requires managed action, requests missing information when needed, and drives actionable items toward a clear outcome.
- Proactivity is a core capability: relevant events can be monitored and surfaced without waiting for an explicit request.

## Non-negotiable constraints

The authoritative checklist lives in **[PRINCIPLES.md](./PRINCIPLES.md)**. Key constraints include:

- Security and guardrails are architectural requirements from the beginning.
- LLM output is never an authorization boundary.
- Prompt injection, indirect injection, phishing, permission abuse, data leakage, and excessive privileges must be considered for every relevant feature.
- Financial, dangerous, sensitive, or irreversible actions require deterministic checks and appropriate user approval.
- **Build vs Reuse:** evaluate shared modules and vetted libraries/providers before writing new generic infrastructure; review security, licensing, maintainability, cost and exit strategy.
- **Engineering rigor:** apply SOLID, KISS, DRY, YAGNI pragmatically; require testable contracts, verified CI quality gates and trustworthy evidence of security controls. See [ENGINEERING_STANDARDS.md](./ENGINEERING_STANDARDS.md).
- Resources are minimized by design: do not use an LLM, expensive model, background process, or continuous polling when a simpler deterministic or event-driven mechanism is sufficient.

## First domain agent: Hrimfaxi (vehicle)

The first concrete domain is vehicle ownership and maintenance. The domain agent is named **Hrimfaxi** (Hrímfaxi); see [CAR_AGENT.md](./CAR_AGENT.md) and [HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md). These are design documents, not implemented code.

Expected areas include vehicle details and history, maintenance and repairs, expenses and budgets, parts and purchases, documents, deadlines, recurring obligations, and observations that can become actionable projects.

Example: a note such as **"the wheel squeaks"** should not remain an isolated note. The agent should determine what information is missing, clarify the desired outcome, create a manageable project or task when appropriate, and help drive it to completion.

## Naming convention

**Heimdall** is reserved for the central orchestrator.

Agents, modules, and major services may use names inspired by Norse mythology when the name meaningfully matches the component's responsibility. The goal is a coherent vocabulary, not mythology for its own sake.

## Documentation ownership

To avoid documents overlapping:

- current position, completed work, next concrete action → **PROGRESS.md**
- product behavior, scope, candidates, open decisions, traceability → **REQUIREMENTS.md**
- stable cross-cutting rules → **PRINCIPLES.md**
- how to apply code-quality practices, testing/CI expectations, standards-gap assessment → **ENGINEERING_STANDARDS.md**
- development sequence and milestones → **PLAN.md**
- exploratory ideas and historical reasoning → **brainstorm.md**
- repository orientation and documentation links → **README.md**
- first agent specification and proposed scenarios → **CAR_AGENT.md**, **HRIMFAXI_USER_CASES.md**
- Hrimfaxi scenario audit and blockers → **HRIMFAXI_CASE_REVIEW.md**

README should point to the source of truth instead of duplicating its details.
