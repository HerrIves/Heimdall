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

- [ ] **Merge PR #5 and protect `main`.** Merge the PROGRESS sync (PR #5) and configure the GitHub Ruleset for `main` with the required `security-gate` check; until then the PR security gate is not enforced ([SECURITY_REVIEW.md](./SECURITY_REVIEW.md)). *Owner action.*
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
- [ ] **SECURITY_REVIEW header is outdated:** it says "proposed policy … in PR branch `security/pr-gate-v1`", but the policy is already in `main`.
- [ ] **Open product questions** (decide and record in REQUIREMENTS):
  - [ ] Single user vs household — who owns data, who approves spending, who gets reminders. More urgent now because Frigg UC-10 tracks family members' location.
  - [ ] DSGVO/GDPR and which data may be sent to external LLM providers (VIN, documents, addresses).
  - [ ] A reference dataset ("golden set") for evaluating the quality of LLM data extraction, so model changes are measurable.
  - [ ] Channel trust — which confirmations are allowed through which channel (app vs Telegram).

## ⚪ Minor

- [ ] **Use-case prefixes:** `CAR-UC-NN` for Hrimfaxi and `HOME-UC-NN` for Frigg (today both use bare `UC-01…` and collide); Fulla already uses `SEC-UC-NN`.
- [ ] **Status only in PROGRESS:** remove the duplicated phase / next-step statements from README, PLAN ("(current)"), REQUIREMENTS ("Next step") and ENGINEERING_STANDARDS §8 and link to [PROGRESS.md](./PROGRESS.md) instead.
- [ ] **PROGRESS:** Frigg has 11 use cases in HOME_USER_CASES, but PROGRESS says 10. PROGRESS also still says `AGENTS.md` does not exist.
- [ ] **SECRETARY_USER_CASES §6:** tick the items already closed by PR #3 (domain vs module split, Fulla name, time vs context, energy axis).

---

## Done

_Move or tick items here with the PR number when they are merged._
