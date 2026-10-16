# Heimdall — Open Tasks (Backlog)

> **What this is:** the list of open documentation and design tasks, ordered by importance. Source: full consistency review of all repository documents on 2026-10-15, after PR #2, #3 and #4 were merged into `main`.
>
> **What this is not:** project status. Current phase and completed work live only in [PROGRESS.md](./PROGRESS.md). Rules for agents and contributors: [AGENTS.md](./AGENTS.md).
>
> **How to use:** each task is done in its own branch and pull request. When a task is merged, tick it here (`[x]`) in the same PR and add the PR number.

---

## 🔴 Critical

- [ ] **Hrimfaxi P0 — inconsistent incident status.** UC-01 writes `status: active_tracking` ([HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md)) and the diagram in [CAR_AGENT.md](./CAR_AGENT.md) §3 uses `ActiveTracking`, but the data model (§2.2) has no such status. Align the model and the scenario (see P0 #2 in [HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md)).
- [ ] **Safety rule before the priority quadrant.** Record the rule "dangerous subsystems (brakes, steering, overheating) → immediate conservative reaction, *before* the Eisenhower quadrant and without waiting for user confirmation" in [SMART_GOALS.md](./SMART_GOALS.md) and REQ-L08 in [REQUIREMENTS.md](./REQUIREMENTS.md). Today they only say "the agent proposes the quadrant, the user confirms it".

## 🟡 Medium

- [ ] **Validate and harden the active `PR_req` Ruleset.** Ruleset for `main` now requires PR and passing `security-gate`, but has `bypass=always` actors (repository role and integration). Review/limit bypass privileges as appropriate, confirm high-risk changes get independent review, and demonstrate that a deliberately unsafe PR cannot be merged. *Owner action; do not assume strict enforcement before this negative test.*
- [ ] **Close the open design conflicts:**
  - [ ] Classification outcomes in REQ-L02: two outcomes — **reference** or **SMART** (RU: *справка / SMART*), not five outcomes and the word "project".
  - [ ] Two levels "incident and SMART goal": the shared SMART goal lifecycle on the platform level plus domain sub-statuses (e.g. Hrimfaxi incident statuses). Record in [CAR_AGENT.md](./CAR_AGENT.md) and [SMART_GOALS.md](./SMART_GOALS.md).
  - [ ] Agent name in running text: use **Hrimfaxi** everywhere, or keep "Car Agent" as an allowed alias (PLAN, PRINCIPLES §23, CAR_AGENT, REQ-L06/D03).
- [ ] **README as entry point:** mention agents **Frigg** and **Fulla**; link [HOME_USER_CASES.md](./HOME_USER_CASES.md) and [SECRETARY_USER_CASES.md](./SECRETARY_USER_CASES.md); describe "domain vs platform module" and the five platform modules; keep one current-phase line and remove the duplicated "Current phase".
- [ ] **SMART_GOALS and GLOSSARY:**
  - [ ] Add the **postponement ladder** (micro-step → fixed slot or delegation → goal graveyard). It exists only in SECRETARY_USER_CASES SEC-UC-04, while GLOSSARY already refers to it in SMART_GOALS Part 1; also update REQ-L08 ("after N postponements → graveyard").
  - [ ] Add the two SMART sizes — **SMART task** (one step, RU: *SMART-задача*) and **SMART goal** (several steps) — and the **SMART passport** (S/M/A/R/T fields). Today they are defined only in SECRETARY_USER_CASES §2.
- [ ] **General payment rule:** move "Heimdall never executes payments itself; it only prepares the data and checks the IBAN against previous payments to the same payee, flagging changes" into [PRINCIPLES.md](./PRINCIPLES.md) or a new REQ-S requirement. Today it lives only inside scenario SEC-UC-01.
- [ ] **German context:**
  - [ ] [HOME_USER_CASES.md](./HOME_USER_CASES.md): replace Russian realities (Пятёрочка, Самокат, Яндекс.Лавка, ЖКХ, управляющая компания) with German ones (Rewe, Lidl, Aldi, Flink, Knuspr, Stadtwerke, Hausverwaltung, Nebenkostenabrechnung).
  - [ ] Hrimfaxi UC-05: replace OSAGO/KASKO with German Kfz-Versicherung (Haftpflicht / Teilkasko / Vollkasko).
- [ ] **SECURITY_REVIEW header is outdated:** it says "proposed policy … in PR branch `security/pr-gate-v1`", but the policy is already in `main`. Update the reference without changing enforcement expectations.
- [ ] **Open product questions** (decide and record in REQUIREMENTS):
  - [ ] Single user vs household — who owns data, who approves spending, who gets reminders. More urgent now because Frigg UC-10 tracks family members' location, and it is the only case that fails the stage flow ([FLOW_CASE_REVIEW.md](./FLOW_CASE_REVIEW.md)).
  - [ ] DSGVO/GDPR and which data may be sent to external LLM providers (VIN, documents, addresses).
  - [ ] A reference dataset ("golden set") for evaluating the quality of LLM data extraction, so model changes are measurable.
  - [ ] Channel trust — which confirmations are allowed through which channel (app vs Telegram).

- [ ] **Flow changes from [FLOW_CASE_REVIEW.md](./FLOW_CASE_REVIEW.md)** (C2 is applied in PRINCIPLES §8, GLOSSARY and REQ-L07; the rest is open):
  - [ ] C1 — fork **query vs input** at capture: read requests are answered from references and create no item.
  - [ ] C3 — **Recurring rules** track (RU: *регламенты*): generator rules with templates create clarified SMART tasks; next due date counts from actual completion. Covers Hrimfaxi UC-06/07 and Frigg UC-03/04/08/09/11.
  - [ ] C4 — **light path** for shopping-list entries and context-only tasks (no SMART passport, no Eisenhower quadrant).
  - [ ] C5 — explicit **"return to formulation"** transition: Slot planner and Review propose step splits, duration changes and micro-steps; the Formulate stage writes them after user confirmation.
  - [ ] C6 — **one owner for lifecycle status** (Tasks module, event-driven) and a mapping table from domain statuses to SMART goal states. Overlaps with "Two levels incident and SMART goal" above and the 🔴 `active_tracking` task.
  - [ ] C7 — **one obligation, one object**: routing and deduplication when a contract or invoice touches two agents (Hrimfaxi UC-03/05, Frigg UC-09, Fulla SEC-UC-01/08).
  - [ ] C8 — **provisional quadrant on arrival**, confirmed at review; for dangerous subsystems the safety rule sets it. Implement together with the 🔴 "Safety rule before the priority quadrant" task.
- [ ] **Habit scenarios:** write 2–3 habit use cases (habit loop, small-change systems) so the habits track can be checked against the flow; today no catalog covers habits.
- [ ] **Eisenhower bottom row:** define review rhythm for "not important" quadrants in [SMART_GOALS.md](./SMART_GOALS.md) §3.

## ⚪ Minor

- [ ] **Use-case prefixes:** `CAR-UC-NN` for Hrimfaxi and `HOME-UC-NN` for Frigg (today both use bare `UC-01…` and collide); Fulla already uses `SEC-UC-NN`.
- [ ] **Status only in PROGRESS:** remove the duplicated phase / next-step statements from README, PLAN ("(current)"), REQUIREMENTS ("Next step") and ENGINEERING_STANDARDS §8 and link to [PROGRESS.md](./PROGRESS.md) instead.
- [ ] **PROGRESS:** Frigg has 11 use cases in HOME_USER_CASES, but an older summary says 10. Update the count and reconcile any remaining outdated summaries.
- [ ] **SECRETARY_USER_CASES §6:** tick the items already closed by PR #3 (domain vs module split, Fulla name, time vs context, energy axis).

---

## Done

- [x] PR #5 merged (status-sync documentation); PR #6 merged (`TODO.md`, `AGENTS.md`). GitHub Ruleset `PR_req` activated on 2026-10-15 and includes `security-gate`; bypass review and negative merge test remain separate open tasks.

_Move or tick items here with the PR number when they are merged._
