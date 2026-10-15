# Heimdall — Brainstorm

> **Brainstorm v1 — frozen.** This file preserves the original product thinking, rationale, and examples that led to Heimdall's design. It is historical context, not a source of active rules.
>
> The authoritative, actively applied rules live in **[PRINCIPLES.md](./PRINCIPLES.md)**; product requirements and the section-by-section traceability of this file live in **[REQUIREMENTS.md](./REQUIREMENTS.md)**; the development sequence lives in **[PLAN.md](./PLAN.md)** and the current status in **[PROGRESS.md](./PROGRESS.md)**. Section numbers below are kept stable because REQUIREMENTS.md refers to them. Where a section overlaps with a principle, it links to PRINCIPLES.md instead of restating it. New ideas go into dedicated design documents (e.g. [SMART_GOALS.md](./SMART_GOALS.md)), not here.

## 1. Vision

Heimdall is a modular, proactive personal assistant that can be delegated complete processes rather than acting only as a chatbot or reminder app.

The system should:

- run continuously, 24/7, independently of a phone or an active chat session;
- proactively monitor tasks, deadlines, budgets, projects, and other relevant state;
- accept natural-language input as well as photos/documents;
- ask follow-up questions when required information is missing or ambiguous;
- turn incoming information into structured data, tasks, schedules, reminders, and domain-specific actions;
- remain independent of a single LLM vendor or model;
- support switching LLM providers/models without changing the business logic;
- be extensible through predefined agents and reusable modules.

## 2. Core concept

Heimdall is a multi-agent system.

### Orchestrator

A central orchestrator receives user requests and system events, determines which existing domain agent is responsible, delegates work, and coordinates results.

Important constraint:

**The orchestrator does not create agents or modules dynamically.**

Agents and modules are developed, tested, and explicitly added to the application. Heimdall is an extensible but finished software system, not a self-generating agent platform.

### Domain agents

An agent represents a complete area of responsibility, not a small technical operation.

Examples:

- Car Agent
- Finance agent
- Project agent
- Home agent

Shopping and Documents were initially also listed here, but they are capabilities used by many agents rather than standalone domains, so they are reusable modules (see §3 and [PRINCIPLES.md](./PRINCIPLES.md) §5).

Each domain agent owns the end-to-end workflow for its domain and may use multiple shared modules.

Example: a Car Agent can manage vehicle data, maintenance, expenses, parts, documents, deadlines, purchases, and reminders.

## 3. Reusable modules

Technical capabilities should be reusable across agents.

Initial candidates:

- Tasks
- Scheduling / calendar
- Notifications / reminders
- Budgeting
- Payments
- Documents
- OCR / image understanding
- File processing
- Web research / monitoring
- Shopping / price search
- External APIs / integrations
- Persistent memory / structured storage

OCR, for example, is not an agent. It is a capability that can be used by the Car Agent, finance agent, project agent, and others.

## 4. Agent template / Agent Factory idea

New domain agents should follow a common architecture.

Prefer a hybrid approach:

- common agent runtime/core;
- reusable module library;
- configuration describing the domain agent;
- custom code only where domain-specific behavior requires it.

The goal is to avoid duplicating infrastructure while not forcing every domain into an overly restrictive configuration system.

New agents are created during development from this common template and then explicitly shipped with Heimdall. They are **not generated at runtime by the orchestrator**.

## 5. Autonomy

The target is a real delegated assistant, not merely an organizer.

Example request:

> “The brake pads need replacing.”

A capable Car Agent should eventually be able to:

1. understand which vehicle is involved;
2. determine urgency and an appropriate deadline;
3. identify compatible parts;
4. research options and prices;
5. estimate the repair cost;
6. check the vehicle budget;
7. create tasks/reminders;
8. monitor whether the work was completed;
9. follow up proactively;
10. update maintenance history after completion.

Actions with real-world consequences — especially purchases and payments — should have explicit authorization boundaries.

We may later define configurable autonomy levels, e.g.:
- observe/analyze;
- propose;
- prepare actions;
- execute approved classes of actions;
- always require confirmation for sensitive actions.

## 6. First reference agent: Car Agent

The first implementation will be an automotive domain agent. It will serve as the reference implementation for the common agent architecture and reusable modules.

Potential responsibilities:

### Vehicle profile
- make/model/version;
- VIN and identifiers;
- registration data;
- mileage;
- technical specifications;
- tires/wheels;
- known installed parts.

### Maintenance
- maintenance history;
- upcoming service;
- inspection deadlines;
- recurring maintenance;
- faults and repairs;
- proactive follow-up.

### Parts
- required parts;
- compatibility;
- alternatives;
- prices;
- purchase status.

### Finance
- vehicle budget;
- repair and maintenance expenses;
- parts;
- insurance;
- taxes;
- fuel/charging;
- budget overruns and forecasts.

### Documents
- invoices;
- receipts;
- inspection reports;
- registration documents;
- insurance documents;
- photos.

### Planning
- tasks;
- deadlines;
- appointments;
- reminders;
- recurring checks.

## 7. Reference workflow

A useful first end-to-end scenario:

**User photographs a repair invoice.**

Possible flow:

1. Car Agent receives the image.
2. Document/OCR module extracts structured information.
3. Agent determines that the document belongs to a vehicle.
4. Repair details are added to maintenance history.
5. Expense is recorded against the vehicle budget.
6. Parts/work performed are recorded.
7. If the invoice implies a future service interval, a task/deadline is created.
8. Notification module schedules the appropriate reminder.
9. Agent reports what changed and asks only for missing/ambiguous information.

This single scenario exercises several reusable modules at once.

## 8. Data and module boundaries

Agents share capabilities, but domain data should have clear ownership and boundaries.

Cross-domain information exchange should be explicit.

Example:
- Car Agent owns vehicle maintenance context.
- A reusable budgeting capability performs calculations/storage primitives.
- A future Finance Agent may provide the global financial view.
- The architecture must define how the car-specific expense contributes to global finances without creating duplicated or conflicting data.

This remains an open design question.

## 9. Reliability principles

Critical behavior must not depend on an LLM remembering to act.

Deterministic infrastructure should handle:

- persistence;
- timers and schedules;
- recurring jobs;
- deadlines;
- event delivery;
- notification delivery;
- authorization rules;
- audit/history where needed.

LLMs should primarily provide reasoning, interpretation, planning, extraction, and natural-language interaction.

## 10. LLM independence

The application should expose an internal model interface rather than coupling agents directly to one provider.

Desired capabilities:

- multiple providers;
- model selection by task;
- fallback models/providers;
- configurable cost/quality trade-offs;
- possibility of local models;
- no domain logic tied to provider-specific APIs where avoidable.

The exact routing strategy and framework are still undecided.

## 11. Possible architecture direction

Current conceptual layers:

1. **Interfaces** — chat, images, documents, later other channels.
2. **Orchestrator** — routing and coordination.
3. **Domain Agents** — complete responsibility areas.
4. **Reusable Modules / Tools** — OCR, tasks, budget, payments, search, notifications, etc.
5. **Event / workflow infrastructure** — proactive execution and communication between components.
6. **Persistence** — structured domain state, history, files, memory.
7. **LLM abstraction** — provider/model-independent reasoning layer.
8. **Integrations** — calendars, payments, shops, external APIs and services.

A shared event mechanism is worth investigating so modules/agents can react to domain events without hard-coding every interaction into the orchestrator.

## 12. Product principles agreed so far

The principles agreed during this brainstorm were consolidated into **[PRINCIPLES.md](./PRINCIPLES.md)** (in particular §1–6, §10, §11, §15 and §23).

One nuance that originated here and is described in §4 above: prefer configuration and shared infrastructure for new agents, but allow custom code where domain-specific behavior requires it.

## 13. Open questions

Before implementation we still need to decide:

- exact scope of the Car Agent MVP;
- module interfaces and contracts;
- agent-to-agent communication;
- ownership of cross-domain data;
- event bus/workflow approach;
- storage model and databases;
- scheduler/job system;
- notification channels;
- permission and autonomy model;
- LLM abstraction/routing;
- agent framework vs custom runtime;
- deployment/runtime environment;
- observability, logs, audit trail;
- secrets and security model;
- monorepo structure and technology stack.

## 14. Next step

Superseded — the current next step is maintained in [PROGRESS.md](./PROGRESS.md).


## 15. Security and guardrails

**Active rules:** [PRINCIPLES.md](./PRINCIPLES.md) §12–17 (security by design, LLM output is not authorization, least privilege, human-in-the-loop, validation before execution, provenance) and §22 (privacy, secrets out of prompts).

**Original rationale:** security became non-negotiable because Heimdall is meant to *perform or prepare real-world actions* — purchases, payments, bookings, account changes — rather than only chat. Once an assistant can act, every piece of external content it reads (web pages, emails, documents, OCR output, tool results) becomes a potential attack path, so guardrails cannot be postponed to a later hardening phase. The dedicated threat model is scheduled in [PLAN.md](./PLAN.md), Phase 6.

## 16. Resource efficiency by design

**Active rule:** [PRINCIPLES.md](./PRINCIPLES.md) §18 (and §21 for event-driven execution).

**Original rationale:** the goal is to minimize resources *without unnecessarily reducing quality or reliability* — efficiency is a design constraint, not a reason to cut corners. Concrete rules (model tiers, caching, context limits, cost telemetry) are deferred to [PLAN.md](./PLAN.md), Phase 7.

## 17. Notes must become actionable or intentionally archived

**Active rules:** [PRINCIPLES.md](./PRINCIPLES.md) §8 (actionable information lifecycle) and §9 (ask only for useful missing information).

**Original thinking:** for actionable observations, the default direction is a **project / outcome-oriented work item** with a clearly defined desired result, rather than a passive note. This applies across domains — Car, Home, Finance, Projects, and future agents.

### Worked example

> “The wheel is squeaking.”

The Car Agent should not merely save this sentence. It should:

1. understand that this may represent a vehicle problem requiring resolution;
2. identify the affected vehicle and relevant context;
3. determine what information is missing;
4. ask focused follow-up questions only where necessary;
5. formulate the desired outcome and success criteria;
6. create a managed project/work item;
7. derive tasks, deadlines, research, diagnostics, appointments, purchases, reminders, or other actions as needed;
8. track the work until the outcome is reached or the project is explicitly cancelled/closed.

### SMART-style outcome definition

The SMART criteria as they were understood here, as a clarification aid:

- **Specific** — what exactly should be achieved;
- **Measurable** — how completion can be verified;
- **Achievable** — whether the outcome is realistically actionable;
- **Relevant** — why it matters / which domain or larger goal it belongs to;
- **Time-bound** — deadline or review point when one is meaningful.

Examples of material that may intentionally stay informational: pure reference information, ideas without current action intent, records, and journal-like notes.

## 18. Norse mythology naming convention

**Active rule:** [PRINCIPLES.md](./PRINCIPLES.md) §24.

**Original thinking:** the convention should communicate architecture and personality rather than decorate. In practice that means:

- do not force a mythological name onto every class, API, table, or utility;
- when designing new agents/modules, actively consider and propose suitable Norse names;
- choose names together with each component's actual responsibilities, not before the architecture is understood.
