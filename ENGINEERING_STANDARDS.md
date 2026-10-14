# Heimdall — Engineering Standards and Best Practices

> **Status:** engineering guidance and gap assessment (2026-10-14). This is **not** certification or evidence of conformity. At present Heimdall is a specification-only project: no application, tests, pipelines or production controls have been verified.
>
> **Authority:** [PRINCIPLES.md](./PRINCIPLES.md) is the mandatory project-level policy; this document describes **how to apply and review it**. [REQUIREMENTS.md](./REQUIREMENTS.md) defines product behavior, [PLAN.md](./PLAN.md) the implementation sequence, [PROGRESS.md](./PROGRESS.md) the current state, and [HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md) scenario-specific gaps.
>
> **Important distinction:** SOLID, KISS, DRY, YAGNI and Clean Architecture are *engineering heuristics / patterns*, not standards with a universal certification procedure. NIST SSDF and OWASP ASVS are published security frameworks/verification references; alignment requires concrete, independently checked evidence. Do not label the project 'compliant' because these documents mention their names.

## 1. Assessment after documentation updates

The **documentation** now explicitly includes engineering principles 26–30. The implementation/test evidence remains absent. “Documented” below means a stated project requirement, **not** that we have validated software compliance.

| Practice or reference | Current documentation | Missing verification / decision | What to do |
| --- | --- | --- | --- |
| Single responsibility / separation of concerns | **Explicit in design policy** (Principles 4–7, 20, 26) | No implemented ownership/dependency checks | Define one responsibility per module, domain ownership and code review rules |
| SOLID (SRP, OCP, LSP, ISP, DIP) | **Explicit in design policy** (Principle 26; section 2 of this guide) | Interface substitutability and dependency direction unverified | Apply SOLID where polymorphism/interfaces matter; require practical contract tests |
| KISS | **Explicit in design policy** (Principles 18–20, 27) | No explicit design simplicity preference | Choose the smallest comprehensible working solution |
| YAGNI | **Explicit in design policy** (Principles 20, 23, 27) | Risk of building multi-agent abstractions and extra services before use | Implement only approved behavior and tested extension points |
| DRY | **Explicit in design policy** (Principles 3–5, 7, 25, 27) | Risk of repeating OCR, billing or notification logic; risk of premature abstraction | One source of truth for stable knowledge; abstract only proven duplication |
| Build vs Reuse | **Documented** (Principle 25) | No chosen components/decision records | Require evidenced license/security/cost/exit review |
| Clean/hexagonal architecture | **Guidance documented**, selection open (Principles 7, 11, 20, 26) | No actual dependency graph or boundaries | Keep domain policy independent of transports, storage, LLM vendors and frameworks |
| Domain-driven ownership | **Partial** (Principles 4, 7) | Finance vs Vehicle source-of-truth unsettled | Design aggregates/events and stable ownership before writing to shared ledgers |
| Automated tests and code quality | **Requirements documented** (Principles 19, 23, 28; Plan 9–10) | No test code, CI, review/coverage policy | Fast unit/domain tests + contracts + integrations + limited user journeys |
| API/event compatibility | **Requirements documented** (Principles 20, 29) | Event schemas, versioning and migration procedures absent | Specify typed contracts and safe evolution |
| NIST SSDF / secure SDLC | **Principles aligned in intent** (12–17, 22, 25, 30) | No secure development process/toolchain, vulnerability response or evidence | Map requirements to SSDF tasks with demonstrable controls |
| OWASP ASVS / LLM threat categories | **Control intent documented** (Principles 12–16, 30; scenario review) | No versioned control checklist, abuse tests or authenticated confirmation implementation | Choose applicable control level, threat model and run relevant tests |
| Twelve-Factor operational ideas | **Guidance documented** (Principles 2, 18, 19, 21, 29) | No configuration, deployment, logging, disaster recovery implementation | Adapt configuration/process/service parity practices to the actual runtime |
| Observability, resilience, release process | **Guidance documented** (Principles 10, 17–19, 29) | No telemetry, rollback or operational runbooks | Design measurable failure signals, recovery, migrations and rollout safeguards |

**Conclusion:** strong product and security intentions, but **implementation maturity is unverified**. The missing practices are actionable engineering and delivery controls, not a reason to redesign the product before choosing its first vertical slice.

## 2. SOLID: practical interpretation

SOLID is useful primarily for object-oriented boundaries and extension points. Apply it to real variation, not every small function or class.

1. **SRP — Single Responsibility.** A class/module should have one coherent reason to change. Hrimfaxi interprets vehicle issues; the shared scheduler executes timers, and the finance ledger records expenses. Do not split every tiny step into a service just to claim SRP.
2. **OCP — Open/Closed.** Support new domain agents, LLM vendors and connector adapters via established contracts without rewriting orchestrator behavior each time. Add an extension seam only once real alternatives exist.
3. **LSP — Liskov Substitution.** A replacement model gateway or storage adapter must respect the same guarantees: errors, output types, timeouts, authorization expectations and cancellation semantics. Verify this with **contract tests** rather than inheritance alone.
4. **ISP — Interface Segregation.** Give an agent only the narrow capabilities it needs. Example: a research tool should not receive write/payment methods; expose read-only research separately from authorized purchase execution.
5. **DIP — Dependency Inversion.** Domain rules depend on stable interfaces, not directly on Telegram, HTTP, a particular ORM, LLM vendor, storage engine, or retailer. Keep the choice of adapters at the composition/infrastructure boundary.

**Anti-pattern:** a universal `AgentInterface` with dozens of methods or a generic framework for agents not yet built. Interfaces should express stable required behavior and clear contracts.

## 3. KISS, YAGNI, DRY, Build vs Reuse

- **KISS:** the smallest *reliable, safe and understandable* implementation wins, not the shortest code. Prefer a modular monolith with explicit boundaries as a **candidate default**, unless deployment/scaling/isolation measurements justify independent services.
- **YAGNI:** do not implement hypothetical agents, speculative microservices, a generic workflow DSL, custom event bus or proprietary OCR until a chosen scenario needs them. Design for evolution with a small number of stable seams.
- **DRY:** eliminate duplication of **knowledge/policy** and proven repeated mechanisms. Two similar-looking vehicle and finance validation rules may be intentionally separate if their domain meaning differs; avoid 'shared' abstractions based only on textual similarity.
- **Build vs Reuse:** search existing internal modules first, then vetted libraries/services/standards. Record functional fit, license, vulnerabilities, data handling, vendor exit, cost and long-term maintenance. Build custom **domain-specific** policy when needed; do not recreate password hashing, cryptography, authentication standards or mature parsing libraries.
- **Refactoring:** do it in small, test-backed steps. Do not conflate a needed behavior change with a broad architectural rewrite.

When these heuristics conflict, prioritize correctness, explicit authorization, safety, observability and maintainable boundaries over minimal line count.

## 4. Contracts and architecture boundaries

- Treat **domain state and invariants** as first-class: approved status values, legal transitions, vehicle ID constraints, evidence, source timestamps, consent, immutable audit semantics only when actually implemented.
- Separate **application orchestration** from **domain logic**, **shared capabilities**, and **infrastructure adapters**. Use clear ports for persistence, scheduling, model invocation, OCR, notification, finances and payments.
- Inputs are validated and normalized at trust boundaries. Internal typed schemas and explicit error results are preferred to unstructured free-form LLM outputs.
- **Version public APIs and events** when consumers depend on them; use backward-compatible evolution and consumer/provider contract tests. Make duplicate/retried messages safe and define concurrency/transaction semantics.
- **One source of truth:** do not store the same expense independently in both Vehicle and Finance. Use linked IDs and deduplicated events, with explicit ownership and reconciliation.
- Track uncertain/inferred facts as such; never promote a guess or AI output silently into verified financial, mileage, mechanical or security-critical facts.

## 5. Testing strategy and Definition of Done (DoD)

Write acceptance scenarios **before** code and test at the cheapest reliable layer:

1. **Unit/domain tests:** invariants, arithmetic/currency/units, status transitions, scheduling rules, approval policy, errors, boundary cases and pure domain decisions. Fast and deterministic.
2. **Contract tests:** model gateway adapters, OCR result schemas, agent/module ports, message consumers, versioning and backward compatibility.
3. **Integration tests:** actual database migration/query behavior, event delivery/outbox, permissions, file store, notification transport and retries; stub unstable paid vendor endpoints.
4. **Targeted end-to-end tests:** one or a few critical user paths, including confirmation, app/Telegram intake, cancellation, persisted follow-up, duplicate requests and restart recovery.
5. **Adversarial tests:** prompt injection through a PDF/web page/image, tool output manipulation, unauthorized purchases, identity confusion, secrets in logs, unexpected model output and low-confidence OCR.
6. **Non-functional tests:** selected performance/cost budgets, load where justified, data restore, backup/recovery, offline/third-party outage handling.

**No universal coverage percentage is mandated.** Measure coverage as diagnostic evidence, not a proxy for quality. Every important regression should have a focused automated test and a reproducible failure case.

**Feature DoD (enforced once implementation begins):**

- [ ] Requirement/UC ID and acceptance criteria linked to the change.
- [ ] Ownership, interface/contracts and Build vs Reuse rationale recorded when material.
- [ ] SOLID/KISS/DRY/YAGNI reviewed **pragmatically**; no unexplained new architecture.
- [ ] Threat model and least-privilege/approval boundaries checked for exposed capabilities.
- [ ] Unit + relevant contract/integration/negative tests **executed and passed**, not merely written.
- [ ] Formatter/linter, type checks, dependency/secrets checks and build succeed in CI.
- [ ] Failure modes, idempotency, cancellation, rollback/retry and relevant telemetry covered.
- [ ] Relevant docs and [PROGRESS.md](./PROGRESS.md) updated; limitations and known issues stated.

Do not mark a feature complete based on Markdown, mock demonstrations, or a green but irrelevant test suite.

## 6. Review, CI/CD and release discipline

**Code review:** prefer small, focused changes; document architectural trade-offs with a short ADR for consequential choices (storage, gateway, event bus, external vendor, auth, financial policies). Discuss *why*, alternatives, and reversibility.

**Quality pipeline (to configure when code exists):**
- reproducible dependency installation with lockfiles and pinned runtime/tool versions;
- formatting, lint, static types, compile/build;
- unit/contract/integration/abuse tests as relevant;
- dependency and secret scanning, license checks where applicable, artifact provenance/release integrity;
- protected main or equivalent review/CI safeguards when collaboration begins;
- migration verification and recoverable, observable rollout (rollback/forward-fix plan);
- branch-level development with a controlled merge process. Exceptions must be explicit.

**Operations:** externalize environment-specific configuration; never commit credentials; limit scopes, expiry and exposure; use structured redacted logs and tracing with correlation IDs, track outcomes/errors/latency/model usage, ensure backups and restore tests where needed, and document recovery procedures. Do not blindly apply every Twelve-Factor item to all infrastructure components.

## 7. Security reference mapping (not certification)

**NIST SSDF SP 800-218 v1.1:** map engineering work to PO (prepare organization/toolchain), PS (protect code/artifacts), PW (secure design/build/test/reuse), RV (vulnerability discovery and response). Current docs describe intent, but no executable evidence exists yet. An **initial public draft** of revision 1 was released in December 2025; a draft must not be silently treated as the final standard.

**OWASP ASVS:** when the web/API implementation exists, select an applicable verification baseline and record control IDs plus tests/evidence. For LLM-enabled flows, add explicit threat scenarios for prompt injection, excessive tool autonomy and data disclosure; choose current OWASP guidance at implementation time. Never claim ASVS/OWASP compliance without verification.

**Twelve-Factor:** useful considerations for service configuration, dependencies, build/release separation, logs and development/production parity; apply only where compatible with durable workflow state and the selected deployment approach.

**References:**
- [NIST SSDF project](https://csrc.nist.gov/projects/ssdf) and [SP 800-218 v1.1](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [Twelve-Factor App](https://12factor.net/)
- [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

## 8. Immediate application to Hrimfaxi

The first agent already demonstrates good decomposition on paper: Hrimfaxi owns vehicle-specific behavior, shared modules provide generic tasks/OCR/scheduler/finance. Before selecting implementation technologies:

1. **KISS + YAGNI:** implement one approved user flow; avoid creating all ten workflows, six agents or a custom orchestration engine immediately.
2. **SOLID + DIP/ISP:** isolate voice/photo intake, domain evaluation, persistence, scheduling, OCR and approval into narrow contracts. A read-only parts search must not possess checkout privileges.
3. **DRY + Build vs Reuse:** no Hrimfaxi-specific reimplementation of OCR, notification queues, authentication, finance ledger or generic task tracking.
4. **Tests and guardrails:** address the safety, canonical-state and double-write findings in [HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md). Use idempotency, partial-failure cases, provenance and abuse tests.
5. **Traceability:** map the selected UC to requirements, code contracts and tests; mark each test as *planned*, *implemented*, or *executed* to avoid false assurance.

**Next decision remains open:** UC-01 (incident tracking) versus UC-03 (invoice processing) for the first MVP; this engineering guidance does not decide product scope.

## 9. When to update this file

Update when a quality rule affects actual design/code practices. Avoid copying long descriptions into README, PLAN or PRINCIPLES. The short mandatory engineering commitments belong in PRINCIPLES; **this file is the practical interpretation and current gap assessment**.
