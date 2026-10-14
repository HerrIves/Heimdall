# Heimdall — Brainstorm

> Living document. This file captures ideas and decisions before we turn them into a formal architecture and implementation plan.

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

- Car agent
- Finance agent
- Project agent
- Home agent
- Shopping agent
- Documents agent

Each domain agent owns the end-to-end workflow for its domain and may use multiple shared modules.

Example: a car agent can manage vehicle data, maintenance, expenses, parts, documents, deadlines, purchases, and reminders.

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

OCR, for example, is not an agent. It is a capability that can be used by the car agent, finance agent, project agent, and others.

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

A capable car agent should eventually be able to:

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

- Proactive by default.
- 24/7 server-side operation.
- Domain agents own complete areas of responsibility.
- Technical capabilities are reusable modules.
- Agents/modules are predefined and explicitly installed, not created dynamically at runtime.
- Start with one domain agent and use it to validate the architecture.
- Car Agent is the first reference implementation.
- Prefer configuration and shared infrastructure, but allow custom code.
- Real-world actions need permission boundaries.
- Critical scheduling/state logic must work independently of the LLM.
- LLM provider/model must be replaceable.

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

Use the Car Agent to define concrete user stories and select one narrow vertical slice for the first MVP. Then derive module contracts and only after that choose the implementation framework and infrastructure.
