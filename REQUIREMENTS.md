# Heimdall — Product Requirements (v0.1)

> **Status:** requirements baseline distilled from [brainstorm.md](./brainstorm.md), not a technical design or claim of implemented features.
> **Scope:** the intended product behavior across all channels and agents. [PRINCIPLES.md](./PRINCIPLES.md) governs *how* components must be designed; [PLAN.md](./PLAN.md) governs *when* work is done.
> **Change rule:** retain provenance and mark assumptions as open, rather than silently treating proposals as decisions.

## Status vocabulary

- **Agreed** — a product-level intention or constraint explicitly agreed in brainstorming; implementation detail may still be open.
- **Candidate** — a suggested feature, workflow, agent, or implementation idea, not yet approved for MVP.
- **Open** — requires a design/product decision.
- **Implemented** — only when verified in running code. **Nothing in this file is implemented yet.**

## 1. Product vision and outcomes

**REQ-V01 · Agreed.** Heimdall is a continuously available, proactive, modular personal assistant that can take responsibility for multi-step outcomes, rather than merely hold conversations or fire one-off reminders.

**REQ-V02 · Agreed.** It runs on server-side infrastructure without depending on an active chat, mobile session, or the availability of a particular LLM provider.

**REQ-V03 · Agreed.** Incoming observations must be classified, preserved, and either intentionally retained as reference material or turned into manageable work with a desired outcome; actionable items must be followed through, not silently abandoned.

**REQ-V04 · Agreed.** Heimdall is the name of the central orchestrator/guardian. Key subsystem and agent names should be chosen from Norse mythology when there is a meaningful correspondence; **the first vehicle agent is named Hrimfaxi (Hrímfaxi)**.

## 2. Entry points and interaction

**REQ-I01 · Agreed.** Different channels reach the **same** Heimdall backend, domain data, workflows, permissions, and state. Presentation or transport adapters must not duplicate business logic.

**REQ-I02 · Agreed.** A dedicated app is the intended full-featured client: capture text, photos, files, and voice; inspect agents, tasks, projects, status, notifications, and settings/approvals. Whether it will be native, PWA, or another technology is **open**.

**REQ-I03 · Agreed.** Telegram is an optional channel that can support quick messages, voice, photos/files, commands, notifications, and relevant interactions. Its exact feature parity with the app is **open**; it must never be required to use the product.

**REQ-I04 · Candidate.** Additional channels include email and other interfaces. Channels may vary in UI convenience and in which security-sensitive actions are allowed.

**REQ-I05 · Agreed.** Heimdall should ask concise follow-up questions only when facts are genuinely missing or uncertain and the answer affects the outcome. A user must be able to correct extracted information.

## 3. Orchestration, agents, and reusable capabilities

**REQ-A01 · Agreed.** The Heimdall orchestrator interprets incoming requests and events, selects **existing** domain agents, coordinates delegated work, and presents results.

**REQ-A02 · Agreed.** Domain agents own a whole life/business domain and its end-to-end workflows (not one technical primitive). Candidate domains: Vehicle, Finance, Project, Home, Shopping, Documents. **Only the Vehicle agent has been chosen as the first reference agent.** The others are possibilities, not a development commitment.

**REQ-A03 · Agreed.** Agents/modules are deliberately built, tested, reviewed, configured, and shipped by developers. The orchestrator must **not generate production agents or modules at runtime**.

**REQ-A04 · Agreed.** Use a shared agent runtime/template plus shared capability modules; add domain-specific code when necessary. The agent “factory” is a **development-time reuse concept**, not dynamic autonomous agent creation.

**REQ-A05 · Candidate module inventory.** Tasks/project tracking, scheduling/calendar, notifications, budget/expenses, payment preparation, documents/file processing, OCR/image understanding, search/research, shopping/price checks, API connectors, persistence/memory. Exact boundaries and contracts remain **open**.

**REQ-A06 · Open.** Agents may need cross-domain information and events. Define ownership and synchronization without duplicate conflicting sources of truth (e.g., a vehicle expense visible in global finances). Decide event-bus vs direct/workflow communication during architecture design.

## 4. Capture → interpretation → outcome lifecycle

**REQ-L01 · Agreed.** Support a quick note, a spoken observation, a photo of a document, or a file as input.

**REQ-L02 · Agreed.** Classify each item as, for example: reference information, a potential action, a problem, a task, or a project. Do **not** mechanically turn all notes into projects.

**REQ-L03 · Agreed.** When actionable, identify domain and context, determine missing information, define a useful desired result, and derive tasks, deadlines, research, appointments, or purchases as appropriate.

**REQ-L04 · Agreed.** Use SMART-style success criteria where helpful (specific, measurable, achievable, relevant, time-bound), but never fabricate deadlines or pointless metrics solely to satisfy SMART.

**REQ-L05 · Agreed.** Track each managed item until completion, explicit cancellation, or another intentional terminal state; allow updates, reassessment, reminders, and corrections.

**REQ-L06 · Candidate acceptance scenario.** The user says “A wheel squeaks.” The Vehicle agent identifies which car and wheel as far as possible, asks meaningful follow-ups, opens a managed investigation/repair work item, records next steps, and tracks the outcome. This is *not* an automatic diagnosis or permission to purchase parts.

## 5. Proactive behavior and workflows

**REQ-P01 · Agreed.** Heimdall can react to persisted dates, tasks, state changes, and external information without the user reopening a client.

**REQ-P02 · Candidate triggers.** Approaching TÜV or service, missed repair task, overspent car budget, lowered part price, invoice due date, incomplete project.

**REQ-P03 · Agreed.** Notifications should be relevant and actionable, with a controlled frequency; support follow-ups and status updates, not just initial alerts.

**REQ-P04 · Agreed.** Deterministic schedules, events, deadlines, persisted job state, and delivery must operate outside LLM prompt-memory. Recovery and duplicate processing require design.

**REQ-P05 · Open.** Actual channels, recurrence semantics, snoozing, escalation, consent, quiet hours, and monitoring rates require product/design decisions.

## 6. The first reference domain: Vehicle

**REQ-C01 · Agreed.** The first end-to-end reference is a vehicle ownership and maintenance agent named **Hrimfaxi (Hrímfaxi)**. Its working specification is [CAR_AGENT.md](./CAR_AGENT.md), with ten candidate scenarios in [HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md).

**REQ-C02 · Candidate scope.** Vehicle records (make/model/version, VIN, mileage, registration, tires, technical characteristics), maintenance/repair history, service/TÜV/inspection deadlines, faults, compatible parts, price research, receipts/invoices/reports, costs/insurance/tax/fuel/charging, recurring checks, and tasks.

**REQ-C03 · Candidate scenario — invoice.** Photo of repair invoice → extract facts → associate with the correct car → present/correct ambiguity → record repair and expense → derive a valid future service item if present → inform user.

**REQ-C04 · Candidate scenario — brake pads.** “Need to replace brake pads” → identify correct vehicle → assess needed follow-up and urgency → research compatible choices/costs → propose plan and budget impact → create tasks/reminders → track completion and update history.

**REQ-C05 · Candidate scenario — fault.** “Wheel squeaks” via voice or chat → actionable investigation → focused questions → diagnostics/research → explicit desired outcome → follow-up until resolved.

**REQ-C06 · Candidate scenario — due maintenance.** Remind about TÜV/service/tire change at an appropriate time; propose preparation steps; track until complete.

**REQ-C07 · Open.** The **first MVP vertical slice** must be selected and documented with inputs, outputs, failure states, authorization, and acceptance checks before writing core implementation. Both fault-report tracking (UC-01, described as MVP slice in the cases catalog) and invoice ingestion (UC-03, described as leading slice in the agent spec/plan) remain candidates until a decision is recorded.

## 7. Autonomy and authorization

**REQ-S01 · Agreed.** Heimdall may analyze, search, monitor, plan, prepare, and carry out only actions permitted by an explicit policy.

**REQ-S02 · Agreed.** Purchases, payments, subscriptions, destructive or consequential account changes and similarly high-risk operations need deterministic authorization controls outside the LLM, with user approval appropriate to the risk.

**REQ-S03 · Open.** Exact autonomy tiers, approval channels, spending caps, identity/session checks, expiration of approvals, and revocation require threat-model and policy design. A message in an untrusted document is never approval.

**REQ-S04 · Agreed.** Review prompt injection (including indirect injection in OCR, pages, files, and tools), phishing, malicious connectors, poisoned memory, data exfiltration, excessive privilege, and forged approvals from the beginning. Do not defer security until implementation is finished.

## 8. Models, reliability, and resource efficiency

**REQ-N01 · Agreed.** Agents should be independent of a single LLM provider/model; a model abstraction must allow switching and fallback. Task-based routing and local models are **candidate options**, not selected architecture.

**REQ-N02 · Agreed.** Use deterministic code when suitable and the smallest sufficient model when an LLM is necessary. Avoid excessive context, duplicated API calls, idle polling, and permanently running LLM loops.

**REQ-N03 · Agreed.** Critical workflows must persist recoverable state, expose failures instead of silently dropping work, and support auditable consequential actions.

**REQ-N04 · Open.** Quantitative reliability, latency, availability, resource and cost budgets, data retention, and observability metrics require later design decisions.

## 9. Documentation and naming conventions

**REQ-D01 · Agreed.** `brainstorm.md` preserves original thinking; `PRINCIPLES.md` is the recurring design checklist; `REQUIREMENTS.md` is the behavior/scope baseline; `PLAN.md` is the sequence of delivery; `README.md` is the navigation and current status.

**REQ-D02 · Agreed.** Architectural choices, security threat model and shared module contracts will live in dedicated documents when those stages start. The initial vehicle-agent specification and scenario review **already exist** in [CAR_AGENT.md](./CAR_AGENT.md), [HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md), and [HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md). Engineering quality guidance is in [ENGINEERING_STANDARDS.md](./ENGINEERING_STANDARDS.md). These documents are not evidence of implemented functionality.

**REQ-D03 · Agreed.** Naming from Norse mythology is a considered preference for meaningful components, not a requirement to rename every file, database table, or helper. The first Vehicle agent's chosen name is **Hrimfaxi**.

## 10. Traceability: original brainstorm → specification / plan / principles

The table below maps **all 18 sections of the existing brainstorm**, including ideas still open; mapping does not mean every detail has been implemented or finally decided.

| Brainstorm section | Where the outcome lives | Status |
| --- | --- | --- |
| 1. Vision | REQ-V01–V03, REQ-I01–I05; Principles 1–3, 8–9 | Agreed baseline |
| 2. Core concept | REQ-A01–A03; Principles 4–7 | Agreed + candidate domains |
| 3. Reusable modules | REQ-A04–A06; Plan phase 4 | Candidate inventory |
| 4. Agent template/factory | REQ-A03–A04; Principles 6, 20, 23; Plan phases 4, 13 | Agreed concept |
| 5. Autonomy | REQ-S01–S03, REQ-C04; Principles 12–16; Plan phase 6 | Agreed constraints; tiers open |
| 6. First Car Agent | REQ-C01–C07; Plan phases 2, 3, 11 | First domain agreed; scope open |
| 7. Invoice workflow | REQ-C03; Plan phases 3, 10 | Candidate |
| 8. Data/module boundaries | REQ-A05–A06; Principles 7, 20; Plan phases 4–5 | Ownership design open |
| 9. Reliability | REQ-P04, REQ-N03; Principles 10, 19, 21; Plan phases 5, 9–10 | Agreed constraint |
| 10. LLM independence | REQ-N01–N02; Principles 11, 18; Plan phases 7–8 | Agreed constraint |
| 11. Architecture direction | REQ-A01–A06, REQ-P04; Plan phases 4–5, 8 | Architectural options open |
| 12. Product principles | Principles 1–24; Plan review gates | Agreed baseline |
| 13. Open questions | REQ-A06, I05, P05, S03, N04; Plan phases 2–9, 12 | Not resolved yet |
| 14. Next step | REQ-C07; Plan phases 2–3 | Next action |
| 15. Security and guardrails | REQ-S01–S04; Principles 12–17, 22; Plan phase 6 + all reviews | Agreed mandatory |
| 16. Resource efficiency | REQ-N02–N04; Principle 18; Plan phase 7 + all reviews | Agreed mandatory |
| 17. Notes → projects/SMART | REQ-L01–L06; Principles 8–9; Plan phases 2–3 | Agreed principle; behavior to detail |
| 18. Norse naming | REQ-V04, D03; Principle 24 | Agreed convention; first name open |

## 11. Outstanding product decisions (not silently closed)

1. ~~Name of the first vehicle domain agent~~ — resolved: **Hrimfaxi**.
2. App delivery technology and the exact Telegram/app feature split.
3. MVP scenario selection and acceptance criteria.
4. Agent/module data ownership and cross-domain synchronization.
5. Notification preferences, delivery and escalation semantics.
6. Autonomy tiers, approval UX and security policy.
7. Exact stack/framework, event infrastructure, persistence, integrations, and hosting.
8. Cost, performance and reliability targets.
9. Which possible future domain agents actually belong to the initial product.

**Next step:** review the initial [CAR_AGENT.md](./CAR_AGENT.md) against these requirements, resolve contradictions with [HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md), and select a narrow end-to-end MVP scenario. Do not mistake this document for an implementation checklist or architecture decision record.
