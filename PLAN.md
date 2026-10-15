# Heimdall — Development Plan

> High-level roadmap from brainstorm to a working personal assistant. This document describes the order of design and implementation. Detailed technical decisions belong in dedicated documents.

## Documentation ownership and review gates

- [brainstorm.md](./brainstorm.md) — original ideas and exploration; Brainstorm v1, frozen.
- [GLOSSARY.md](./GLOSSARY.md) — shared vocabulary (SMART goal, reference, task, agent, module, event).
- [REQUIREMENTS.md](./REQUIREMENTS.md) — product behavior, candidate scope, open decisions, and traceability back to every brainstorm section.
- [PRINCIPLES.md](./PRINCIPLES.md) — binding cross-cutting design principles and component checklist.
- [ENGINEERING_STANDARDS.md](./ENGINEERING_STANDARDS.md) — pragmatic SOLID/KISS/DRY/YAGNI guidance, quality gates and standards-gap assessment.
- [SECURITY_REVIEW.md](./SECURITY_REVIEW.md) — mandatory PR security review, threat categories and GitHub Ruleset activation.
- **This file** — phases, sequencing, deliverables, and completion gates; not a second copy of requirements.
- [README.md](./README.md) — navigation and project status.

**Mandatory gates for every phase and new agent/module/integration:** (1) verify relevant requirements and mark each as agreed, candidate or open; (2) review PRINCIPLES, ENGINEERING_STANDARDS and SECURITY_REVIEW, including threat model/prompt injection, least privilege, authorization, Build vs Reuse, KISS/YAGNI/DRY/SOLID, resource efficiency, reliability and data ownership; (3) define observable acceptance tests and failure behavior; (4) document new decisions and unresolved issues; (5) update README/status and the requirements traceability when scope changes. No phase is marked complete based solely on writing a document.

## Current status

- [x] Initial product brainstorm
- [x] Core product principles
- [x] Domain-agent concept
- [x] Reusable-module concept
- [x] Proactive / 24×7 direction
- [x] LLM-provider independence
- [x] Security and guardrails as a first-class requirement
- [x] Resource-efficiency principle
- [x] Initial requirements traceability audit (`REQUIREMENTS.md`)
- [ ] Define and build the first reference agent

---

## Phase 1 — Close Brainstorm v1 ✅

`brainstorm.md` is the origin of Heimdall's product ideas. Its agreed content has been consolidated into dedicated documents, and Brainstorm v1 is now frozen as historical context.

The topics this phase required to be captured are covered as follows:

- multi-channel interaction, mobile app, Telegram, one backend behind all channels → [PRINCIPLES.md](./PRINCIPLES.md) §2–3 and REQ-I01–I04 in [REQUIREMENTS.md](./REQUIREMENTS.md); client details in Phase 12 below;
- proactive behavior and triggers → PRINCIPLES §1, §21; REQ-P01–P05;
- human-in-the-loop and authorization boundaries → PRINCIPLES §13, §15; REQ-S01–S03;
- security / guardrails → PRINCIPLES §12–17; REQ-S04;
- resource efficiency → PRINCIPLES §18; REQ-N02.

New ideas and implementation details go into dedicated design documents, not into the brainstorm.

**Result:** `brainstorm.md` — Brainstorm v1 complete and frozen.

---

## Phase 2 — Define the Hrimfaxi Vehicle Domain Agent (draft produced)

Use the Car Agent as the first reference domain agent.

Create the first agent's behavioral specification (`CAR_AGENT.md`, for **Hrimfaxi**) using `REQUIREMENTS.md`. Describe what it should do in real life before deciding how it is implemented. Capture acceptance criteria and how notes become managed outcomes.

Define:

- responsibilities and boundaries;
- vehicle profile;
- maintenance and service history;
- faults and repairs;
- documents;
- expenses and vehicle budget;
- parts and purchases;
- tasks, deadlines and recurring maintenance;
- proactive monitoring;
- interaction with the user;
- authorization boundaries.

Describe concrete end-to-end user stories, for example:

- photograph a repair invoice;
- report a new fault by voice;
- “I need to replace the brake pads”;
- upcoming TÜV / inspection;
- tire change;
- search for a compatible part;
- record fuel/charging or repair expense;
- remind and follow up until maintenance is completed.

**Gate:** every chosen scope item must trace to an explicit requirement or newly reviewed decision; include SMART-style note-to-work lifecycle, channel behavior, threat cases, permissions and resource constraints.

**Result:** a clear behavioral specification for the first agent.

---

## Phase 3 — Select the first vertical slice (current)

Do not attempt to implement the entire Car Agent at once.

Choose one narrow scenario that exercises the architecture end-to-end.

Candidates documented in [HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md): **UC-01 (fault report → tracked incident)** and **UC-03 (invoice photo → structured service history)**. The catalog provisionally labels UC-01 as a first slice; [CAR_AGENT.md](./CAR_AGENT.md) describes invoice ingestion as the leading slice. **Decision pending** — neither has been formally accepted.

Invoice candidate:

> User sends a photo of a vehicle repair invoice → Heimdall extracts the data → identifies the vehicle → records maintenance and expense → creates any relevant future task → reports the result and asks only for missing information.

Define:

- input;
- expected structured data;
- decisions the agent makes;
- modules involved;
- persistent state changes;
- events produced;
- user confirmations;
- output;
- failure/ambiguity paths.

**Guardrail gate:** review [HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md), resolve critical unsafe assumptions and record Build vs Reuse decisions; a specification review is not a runtime test.

**Gate:** demonstrate the entire capture → classification → reference / SMART goal → tracking lifecycle when relevant, including errors, human approvals, retries and notification behavior; record the acceptance tests.

**Result:** first implementable Heimdall workflow.

---

## Phase 4 — Derive reusable modules and contracts

Use the Car Agent scenarios to determine which capabilities belong in shared infrastructure.

Likely modules:

- Tasks;
- Scheduler;
- Notifications;
- Documents;
- OCR / image understanding;
- Budget / expenses;
- Search / research;
- Shopping;
- Context provider (place and available time from voice, geolocation, NFC — candidate, see [SMART_GOALS.md](./SMART_GOALS.md));
- Payments;
- persistent storage / memory;
- integrations.

For every module define:

- responsibility;
- inputs/outputs;
- permissions;
- events;
- persistence requirements;
- failure behavior;
- security boundaries.

Avoid creating abstractions without a concrete use case.

**Result:** stable contracts between agents and reusable capabilities.

---

## Phase 5 — Define the core architecture

Create `ARCHITECTURE.md`.

Specify:

- interface/channel layer;
- orchestrator;
- agent runtime;
- domain agents;
- module/tool layer;
- event/workflow system;
- scheduler;
- persistence;
- file/document storage;
- LLM abstraction;
- integrations;
- notification delivery;
- authorization/policy layer;
- audit trail and observability.

Resolve cross-domain ownership, especially questions such as how a Car Agent expense contributes to the future global Finance domain without duplicated state.

**Runtime security test planning:** identify executable model-to-tool trust boundaries and design threat-driven test fixtures covering prompt injection, tampered/spoofed tool responses, forged approvals, cross-agent data access and unauthorized side effects. Record expected deterministic denial and observable evidence. The tests are planned here, not claimed executed.

**Gate:** document the decision status (accepted vs candidate), component trust boundaries, cross-domain data ownership and multi-channel consistency; audit against PRINCIPLES.md.

**Result:** Heimdall architecture v1.

---

## Phase 6 — Threat model and guardrails

Create a dedicated security design before enabling consequential actions.

Cover at minimum:

- direct and indirect prompt injection;
- malicious web/document/email/image content;
- phishing/social engineering;
- untrusted tool output;
- data exfiltration;
- permission escalation;
- poisoned memory;
- secrets management;
- user/session identity;
- action authorization;
- purchases and payments;
- auditability.

Define deterministic policy enforcement outside the LLM.

Classify operations by risk and specify which can run automatically and which require confirmation.

**Test specification gate:** enumerate negative/adversarial scenarios and acceptance criteria for each enabled tool, permission scope, model gateway and untrusted input. Define which failures block release. See [SECURITY_REVIEW.md](./SECURITY_REVIEW.md). 

**Result:** security model and permission system.

---

## Phase 7 — Resource and cost model

Translate the resource-efficiency principle into technical rules.

Decide:

- when no LLM is needed;
- model tiers for different tasks;
- context limits and retrieval strategy;
- caching;
- event-driven vs continuously running processes;
- API-call minimization;
- background-job strategy;
- storage lifecycle;
- cost telemetry and limits.

**Result:** predictable infrastructure and LLM operating costs.

---

## Phase 8 — Choose the technology stack

Only after the behavioral and architectural requirements are known, evaluate concrete technologies.

Decide:

- backend language/framework;
- agent/runtime framework vs custom implementation;
- database(s);
- event/workflow technology;
- scheduler;
- object/file storage;
- LLM gateway/provider abstraction;
- mobile client technology;
- Telegram integration;
- deployment/container platform;
- monitoring/logging;
- CI/CD.

Evaluate candidates against Heimdall's actual requirements rather than choosing a framework first.

**Result:** documented stack decisions and rationale.

---

## Phase 9 — Repository and engineering foundation

Create the initial repository structure.

Set up:

- monorepo/repository layout;
- shared contracts;
- configuration;
- local development environment;
- containers;
- database migrations;
- secrets handling;
- testing strategy;
- CI;
- logging/observability baseline;
- security checks.

**Security PR gate:** before merging into protected `main`, require `security-gate` in the GitHub Ruleset and review whether code scanning, dependency checks, provenance and prompt-injection runtime tests apply. The workflow alone does not create an enforceable branch rule.

**Executable-agent security harness:** when model-to-tool interfaces become runnable, wire deterministic adversarial fixtures, mocked/sandboxed tool handlers and policy-denial assertions into CI. Do not defer these tests until all agents have been implemented. A PR adding an executable agent/tool boundary must include the tests for its threats.

**Engineering gate:** CI must run formatting/lint, static types, builds, focused tests and suitable dependency/secrets checks once code exists. Define reproducible dependency versions, code review criteria and documented release/migration procedures. Do not mark checks implemented before they execute successfully.

**Result:** runnable Heimdall skeleton.

---

## Phase 10 — Implement the first vertical slice

Implement the selected Car Agent workflow end-to-end.

The goal is not a demo with mocked architecture, but a small real system that validates:

- channel → orchestrator → agent routing;
- LLM abstraction;
- module calls;
- persistence;
- events/tasks;
- permissions;
- notifications;
- audit trail;
- failure handling.

**Engineering gate:** trace UC/requirements to executed unit, contract, integration, adversarial and selected end-to-end tests. Validate API/event compatibility, state invariants, retries/idempotency, observability and recovery, following [ENGINEERING_STANDARDS.md](./ENGINEERING_STANDARDS.md).

**Mandatory LLM security release gate:** exercise the runnable agent against hostile prompts/documents/retrieval/tool results, tool impersonation, forged user approvals, cross-agent data leakage and unauthorized external actions. Verify *actual* blocked tool calls and absent side effects, not only that the model says "no". Relevant tests must run and pass in required CI checks before the first agent is considered complete or deployable. No production secrets or payments in test environments.

**Result:** first working Heimdall workflow.

---

## Phase 11 — Expand the Car Agent

Iteratively add the remaining validated Car Agent scenarios.

Possible order:

1. vehicle profile;
2. maintenance history;
3. tasks and reminders;
4. document ingestion;
5. expenses/budget;
6. proactive maintenance;
7. parts research;
8. shopping;
9. approved external actions.

Continuously refine shared modules instead of duplicating capabilities inside the agent.

**Result:** useful Car Agent MVP.

---

## Phase 12 — Build user interfaces (deliver a minimal capture channel early in phase 10)

Develop clients against the same Heimdall backend. **A minimal usable intake/notification channel is required for phase 10**; full app and Telegram client experiences may arrive later. Do not mistake this ordering for delaying all interaction until phase 12.

### Mobile app

Full interaction and management interface:

- text;
- voice;
- camera;
- files;
- tasks;
- agents;
- notifications;
- structured domain views;
- settings and permissions.

### Telegram

Optional lightweight channel for:

- messages;
- voice;
- photos/documents;
- quick commands;
- proactive notifications;
- approvals where appropriate and secure.

Channels contain presentation/integration logic, not domain business logic.

**Result:** Heimdall can be used naturally from more than one interface.

---

## Phase 13 — Validate the Agent Template

Once the Car Agent is useful, extract the proven common structure into the reusable agent template/runtime.

Then create a second domain agent — likely Finance, Home, Project, or another high-value domain — to test whether the abstraction actually generalizes.

Do not declare the agent architecture reusable until a second agent successfully uses it.

**Result:** validated Agent Factory / domain-agent architecture.

---

## Phase 14 — Expand Heimdall

Add further agents and integrations incrementally.

For every new agent/module:

1. define real user scenarios;
2. define ownership and boundaries;
3. reuse existing modules where possible;
4. perform threat-model/security review;
5. define permissions;
6. estimate resource/cost impact;
7. test deterministic behavior;
8. add proactive behavior only where useful.

**Result:** a growing but controlled personal-assistant platform.

---

## Immediate next step

Review [CAR_AGENT.md](./CAR_AGENT.md) and [HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md) for consistency and safety. The name **Hrimfaxi** and draft specification are recorded; next decide between UC-01 and UC-03 as the initial MVP slice, then define explicit acceptance tests. Keep all requirements and principles traceable.

Do **not** choose the agent framework or implementation stack yet. The first Car Agent scenarios should drive those decisions.
