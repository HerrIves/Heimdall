# Hrimfaxi — Scenario Compliance & Guardrail Review

> Review date: 2026-10-14. Scope: all ten scenarios in [HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md), reviewed against [CAR_AGENT.md](./CAR_AGENT.md), [REQUIREMENTS.md](./REQUIREMENTS.md), and [PRINCIPLES.md](./PRINCIPLES.md). **This is design/static scenario analysis, not execution of code or automated tests.** No scenario is yet implementation-ready.

## Status rubric

- **Aligned** — main intent and ownership match product specification (does not mean implemented).
- **Partial** — intent matches, but critical acceptance, consistency or guardrail gaps remain.
- **Blocked** — an unsafe or contradictory rule must be corrected before implementation.
- **Build vs Reuse** — proposed division between vehicle-domain logic (Build) and common modules / evaluated third-party capability (Reuse). No provider has been selected.

| Case | Spec reference | Review | Key missing guardrail or contradiction | Build (domain-specific) | Reuse (capability) |
| --- | --- | --- | --- | --- | --- |
| **UC-01** Brake squeak | REQ-C05, REQ-L01–L05; Incident lifecycle | **Blocked** | High-severity brake symptom treated as ordinary 48-hour follow-up; `active_tracking` mismatches canonical `Incident.status`; must support provisional record, urgent triage and verified closure | Vehicle fault triage rules, incident-context interpretation | Shared intake, task store, scheduler, notification, audit |
| **UC-02** Dashboard/OBD-II | REQ-C05; safety constraints | **Blocked** | Red/yellow indicator color is not proof of drivability; vision errors, vehicle-specific manual, urgent signs and no-connection behavior need handling | Vehicle-specific hazard explanation, uncertainty handling | Image recognition, reference retrieval, tasks |
| **UC-03** Service invoice | REQ-C03; maintenance and expenses | **Partial** | Low OCR confidence, missing VIN, duplicate import, injection in text, historical vs current mileage, partial writes, replayed expenses | Line-item interpretation, correct vehicle match, service facts | Documents/OCR, storage, finance ledger, dedupe/outbox, approval |
| **UC-04** Fuel/charging receipt | REQ-C02; finance | **Partial** | No trustworthy full-tank baseline; estimates could be reported as precise; duplicate receipts, units/currency and partial charging sessions | Consumption methodology and units | OCR, expense ledger, analytics |
| **UC-05** Insurance/TÜV | REQ-C06, P03, S04 | **Partial** | Contains region-inappropriate OSAGO/KASKO terms for German-default examples; policy dates/renewal assumptions, identity of emergency numbers, privacy and 30/7 day fixed reminders | Local regulatory/policy date interpretation | OCR, secure documents, scheduler, private lookup |
| **UC-06** Scheduled maintenance | REQ-C06, P01–P05 | **Partial** | 15,000 km/365d examples not vehicle-specific rules; estimated mileage uncertainty, missing odometer samples, reminder storm and idempotency | Service interval applicability and projections | Scheduler, notification, event persistence |
| **UC-07** Seasonal tires | REQ-C06, P03 | **Partial** | +7°C heuristic not legal mandate, location/season differing, storage and tread evidence uncertain, weather access and user preferences undefined | Tire-state interpretation and country/vehicle-specific constraints | Weather adapter, calendar, tasks, notifications |
| **UC-08** Parts research | REQ-C04, S01–S04 | **Partial** | Claimed “OEM guarantee/verified fit” overstates confidence; VIN privacy, supplier manipulation, injected shopping instructions, user-approved checkout required | Evidence-backed vehicle fitment and safe recommendation | Search, retailer adapters, approval, budget |
| **UC-09** Total cost | REQ-C02, A06 | **Partial** | Finance ownership, duplicate expenses, missing categories, uncertain periods, user privacy and projections not specified | Vehicle-specific cost aggregation definitions | Shared ledger, analytics, reporting |
| **UC-10** Service passport | REQ-C02, S04, D02 | **Partial** | PDF called tamper-evident without signature; invoice authenticity unverified; VIN/address leakage, export consent, omissions, provenance | Vehicle maintenance narrative, selection of entries | Document export, secure file access, redaction, audit |

## High-priority cross-case defects

1. **Safety advice (P0):** UC-01 and UC-02 must not suggest wait-and-see or “safe to drive” based on brake noise, light color, OCR, historical part replacement or incomplete evidence. Provide conservative symptom-specific escalation with uncertainty; prioritize qualified assessment.
2. **Inconsistent state transitions (P0):** `Incident` defines `new → triaged → investigating → action_scheduled → resolved → closed`, while UC-01 writes `active_tracking` and the diagram uses `ActiveTracking`. Define one persisted enum, a separate process diagram and terminal/cancelled states, with recoverable ambiguous intake.
3. **Injection/untrusted input (P0):** Invoice text, diagnostic PDFs, car manuals, supplier pages and visual OCR may include hostile instructions. Sandboxing/sanitization alone is not sufficient: strict trust separation, schema validation, least-privilege tools and policy checks outside LLM.
4. **Duplicate/corrupt writes (P0):** Any replay of UC-03/04/09 must not duplicate expenses; records need stable IDs, source provenance, deduplication and transaction/outbox semantics with retries and compensating corrections.
5. **Consent/permissions (P0):** Purchases, payments, bookings with commitments and external data disclosure require valid policy and authenticated confirmation; compare/search is not implicit checkout consent.
6. **Reference certainty (P1):** Sample mileage and timelines are not system defaults. VIN fitment and OCR fields require source evidence/uncertainty. Distinguish historical vs current mileage and configured vs estimated deadlines.
7. **Privacy (P1):** VIN, registration numbers, policy data and buyer-facing PDFs require purpose limitations, secure channel controls, redaction and controlled access.
8. **MVP conflict (P1):** UC-01 is labeled MVP in the catalog, whereas UC-03 is framed as leading in the specification. Both remain options until explicitly selected.
9. **Incomplete outcome lifecycle (P1):** Most scenarios do not show project/work-item status, pause/cancel/reopen, missing-data flow, owner, verified completion, or escalation. Requires per-case criteria.
10. **German context (P2):** UC-05 currently uses OSAGO/KASKO as generic examples; scope must be locale-aware and support Germany's policy/TÜV terms without asserting universality.

## Build vs Reuse decision record (design proposal; not package selection)

| Capability | Default approach | Reason / review gate |
| --- | --- | --- |
| Heimdall Tasks/Projects, Scheduler, Notifications, Audit | **Reuse internal shared modules**; evaluate established infrastructure behind interfaces | Cross-domain behavior, deterministic execution, idempotency; do not create per-agent copies |
| OCR / vision, PDF export, weather, retailer lookup | **Reuse evaluated libraries/providers through adapters** | Compare accuracy, licensing, data minimization, availability, cost, supply-chain and vendor exit; no chosen vendors yet |
| Expense ledger, authorization, identity | **Reuse one shared platform capability / vetted foundation** | Avoid duplicate finance truth and separate payment authority from LLM |
| Vehicle profile, symptom/risk policies, service interval applicability, fitment evidence | **Build Hrimfaxi-specific rules and workflows** | These are domain-specific differentiators requiring reliable vehicle context |
| AI model invocation | **Reuse shared model gateway** | Provider independence, resource caps and failures |
| Safety/approval policy | **Never delegate enforcement to an LLM or third-party content** | Deterministic policy and authenticated approval; reuse enforcement mechanism, build policy configuration as needed |

A Build vs Reuse selection **must** document evaluated candidates, license, threat model, privacy/data residency, operational burden, resource cost, maintenance, lock-in, failure behavior and rationale. Reuse is not proof of security.

## Proposed per-case acceptance checks (to turn into actual tests later)

- **UC-01:** unknown car → saved provisional incident; severe brake symptoms → immediate conservative advice; duplicate report → one incident / linked updates; no unapproved order; valid state transitions; closure requires evidence or explicit confirmation.
- **UC-02:** unreadable warning photo → request clarification; ambiguous indicator → never claim safe driving; critical symptoms → priority escalation; manual unavailable → acknowledge uncertainty.
- **UC-03:** low-confidence OCR → draft, no silent write; historical invoice → current mileage unchanged; malicious instructions in invoice → never executed; duplicate upload/retry → exactly one expense; partial failure → recoverable state.
- **UC-04:** missing full-tank pair → no invented consumption; mixed liters/kWh → correct units; duplicates/returns → correct ledger semantics; receipt lacks vehicle → clarification.
- **UC-05:** missing or conflicting dates → no invented expiry; wrong jurisdiction → localization; untrusted Telegram requester → no disclosure of insurance details; reminder suppression/snooze respected.
- **UC-06:** sparse odometer history → estimated mileage labeled uncertain; manufacturer rules unavailable → no invented service intervals; reminders retried without duplication.
- **UC-07:** no weather integration → calendar-based fallback; +7°C treated as heuristic; multiple tire sets/storage uncertainty → ask only useful question; no paid appointment auto-booked.
- **UC-08:** multiple vehicle trim variants → no “verified fit” until proof; malicious seller page cannot trigger checkout; VIN never leaked by default; price stale/availability unknown marked accordingly.
- **UC-09:** overlapping expense categories → no double count; missing invoices → incomplete coverage displayed; currency conversion/period explicit; permission boundaries observed.
- **UC-10:** invalid or unverified invoices → flagged as unverified; export strips sensitive identifiers; no false tamper-proof label; export destination requires approval; access audited.

## Exit criteria before any UC is build-ready

1. Choose target case and agree behavior/acceptance criteria.
2. Define canonical input/output schema, state machine and failure paths.
3. Perform threat review for all untrusted sources, sensitive actions and external integrations.
4. Validate permissions, provenance, deduplication, confirmation and data ownership.
5. Record Build vs Reuse decision for every required capability.
6. Implement and **execute** tests covering normal, invalid, adversarial and recovery paths.
7. Update [PROGRESS.md](./PROGRESS.md) only upon verified completion.

## Conclusion

**Design alignment:** 10/10 cases align with Hrimfaxi's intended domain at a high level. **Safety and readiness:** 2 blocked by safety-critical claims/logic, 8 partial; 0 approved as implementation-ready. This is a document review, not a claim of simulated or runtime execution. Correct high-risk assumptions and define acceptance/guardrails before choosing a production MVP.
