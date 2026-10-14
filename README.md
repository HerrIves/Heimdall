# Heimdall

**Heimdall** is a modular, proactive personal assistant platform.

Heimdall is the central orchestrator: one brain, multiple channels and specialized domain agents. The name refers to Heimdall, the watchman of Norse mythology, reflecting the system's goal of observing relevant events, noticing them early, and proactively helping the user.

## Project status

**Current phase:** concept and requirements definition.

The brainstorming and initial requirements-to-principles/plan audit are complete. The next focus is defining the first **vehicle domain agent**, a working label until its Norse-inspired name is chosen, with end-to-end scenarios and acceptance criteria before selecting a technical stack.

## Start here

1. **[REQUIREMENTS.md](./REQUIREMENTS.md)** — product behaviors, scoped/candidate ideas, open decisions and mapping of all 18 brainstorm sections.
2. **[PRINCIPLES.md](./PRINCIPLES.md)** — mandatory rules and the component-review checklist.
3. **[PLAN.md](./PLAN.md)** — the delivery roadmap, milestones and review gates.
4. **[brainstorm.md](./brainstorm.md)** — original ideas and their rationale; preserved for historical context.
5. **README.md** — this document: navigation and current project status.

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
- Resources are minimized by design: do not use an LLM, expensive model, background process, or continuous polling when a simpler deterministic or event-driven mechanism is sufficient.

## First domain agent: Vehicle (working label; name undecided)

The first concrete domain is vehicle ownership and maintenance.

Expected areas include vehicle details and history, maintenance and repairs, expenses and budgets, parts and purchases, documents, deadlines, recurring obligations, and observations that can become actionable projects.

Example: a note such as **"the wheel squeaks"** should not remain an isolated note. The agent should determine what information is missing, clarify the desired outcome, create a manageable project or task when appropriate, and help drive it to completion.

## Naming convention

**Heimdall** is reserved for the central orchestrator.

Agents, modules, and major services may use names inspired by Norse mythology when the name meaningfully matches the component's responsibility. The goal is a coherent vocabulary, not mythology for its own sake.

## Documentation ownership

To avoid documents overlapping:

- product behavior, scope, candidates, open decisions, traceability → **REQUIREMENTS.md**
- stable cross-cutting rules → **PRINCIPLES.md**
- development sequence and milestones → **PLAN.md**
- exploratory ideas and historical reasoning → **brainstorm.md**
- repository orientation and current focus → **README.md**
- agent-specific requirements and scenarios → dedicated agent documents as they are created

README should point to the source of truth instead of duplicating its details.
