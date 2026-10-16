# Flow Case Review — all scenarios run through the stage flow

> **Status:** analysis, draft. Checked on 2026-10-16. No code exists; this is a paper check of the design, not a test result.
> **Scope:** all 33 scenarios — Hrimfaxi UC-01…10 ([HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md)), Frigg UC-01…11 ([HOME_USER_CASES.md](./HOME_USER_CASES.md)), Fulla SEC-UC-01…12 ([SECRETARY_USER_CASES.md](./SECRETARY_USER_CASES.md)).
> **Checked against:** (1) the stage flow with six stages and five rules (sections 1–6), built from GTD, SMART and the Eisenhower matrix; (2) the SMART practices and depth levels of [SMART_GOALS.md](./SMART_GOALS.md) Part 4 (section 7).
> **Related:** classification rule [PRINCIPLES.md](./PRINCIPLES.md) §8, terms [GLOSSARY.md](./GLOSSARY.md), requirements REQ-L07–L09 in [REQUIREMENTS.md](./REQUIREMENTS.md), Hrimfaxi safety audit [HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md). Open follow-up tasks live in [TODO.md](./TODO.md); project status lives in [PROGRESS.md](./PROGRESS.md).

---

## 1. The flow under review (version 1)

Idea: split the flow into stages. Each stage answers **one question**, uses **one method**, and has **one owner**. Contradictions appear when two methods answer the same question; separating the questions by stage removes the overlap.

```
Safety — fires before any stage
   │
1. Capture ─▶ 2. Clarify ─▶ 3. Formulate ─▶ 4. Prioritize ─▶ 5. Engage ─▶ 6. Review
   GTD           GTD           SMART           Eisenhower       GTD           GTD
                 reference or  task or goal    weekly, at       context,      day, week,
                 SMART goal                    goal level       time, energy  quarter
```

| # | Rule | RU |
|---|---|---|
| R1 | Each field is written by exactly one stage; the others only read it | *одно поле — один писатель* |
| R2 | Precedence when rules conflict: safety → hard deadlines → explicit user decision → method rule → LLM suggestion | *лестница старшинства* |
| R3 | Eisenhower picks the goals for the week (at review); the four GTD criteria pick the next action in the moment | — |
| R4 | Habits run on their own track; their time is reserved first, inside the 80% load limit ([SMART_GOALS.md](./SMART_GOALS.md) §11) | *привычки — отдельная дорожка* |
| R5 | A domain agent supplies facts, not priorities ([GLOSSARY.md](./GLOSSARY.md): domain vs platform module) | *домен даёт факты* |

Legend: ✅ passes as is · ⚠️ passes only after a flow change (numbered C1–C8, section 3) · ❌ does not work, needs a product decision.

---

## 2. Scenario run

### Hrimfaxi — vehicle

| ID | Scenario | Path through the stages | Result |
|---|---|---|---|
| UC-01 | Brakes squeak | Safety (R2) fires first → clarify: incident (domain fact) + SMART goal "diagnosis" → the quadrant is set by the safety rule, not proposed → review daily. Two state machines: incident (domain) and SMART goal (platform) | ⚠️ C2, C6, C8 |
| UC-02 | Check Engine / OBD code | As UC-01, plus an immediate checklist answer (oil, coolant temperature) before formulation | ⚠️ C2, C8 |
| UC-03 | Service invoice | One document yields four objects: MaintenanceLog entry (reference), expense (reference / finance), recommendation "rear pads 20%" (future SMART task), obligation to pay (SMART task in the Fulla flow) | ⚠️ C2, C7 |
| UC-04 | Fuel receipt | Clarify → reference (expense, consumption). No further stages needed | ✅ |
| UC-05 | Insurance / TÜV | Document → reference; renewal → SMART task. Overlaps with SEC-UC-08 (cancelling the same policy): two agents create two reminders for one contract. "Towing number" is a query, not an input | ⚠️ C1, C7 |
| UC-06 | Scheduled service | Not a user input but a recurring rule that creates the task itself | ⚠️ C3 |
| UC-07 | Seasonal tire swap | Same: a season / weather rule creates the task | ⚠️ C3 |
| UC-08 | Part research | SMART task → research → purchase only with approval (R2, level 1). No field-ownership conflict | ✅ |
| UC-09 | Total cost of ownership | A read request, not an input: nothing is created | ⚠️ C1 |
| UC-10 | Service passport for resale | Read request + export with approval | ⚠️ C1 |

### Frigg — home

| ID | Scenario | Path through the stages | Result |
|---|---|---|---|
| UC-01 | Staple discount watcher | The input comes from the system (catalog), not the user → clarify via user confirmation. A shopping-list entry is not a SMART goal and needs no Eisenhower quadrant | ⚠️ C4 |
| UC-02 | Photo of packaging → list | List entry, triggered by the context "in the shop". Running it through S/M/A/R/T and a quadrant is overkill | ⚠️ C4 |
| UC-03 | Pantry low stock | Generator rule from consumption rate → list entry | ⚠️ C3, C4 |
| UC-04 | Floating cleaning interval | Generator rule; the next interval counts from actual completion. "Not today" → Engage moves the slot; no rule broken | ⚠️ C3 |
| UC-05 | Loose cabinet handle | Clarify → SMART task, context "home", energy "routine" → batched into a "home hour" at stage 5 | ✅ |
| UC-06 | Dog soiled the sofa | First an immediate first-aid answer, then an urgent SMART task with branches (self / cleaning service / rental), purchases with approval. Urgent but not a safety case: the quadrant is needed now, not at the weekly review | ⚠️ C2, C8 |
| UC-07 | Appliance passport | Clarify → reference. "What does error E18 mean" is a read request | ✅ |
| UC-08 | Appliance care cycles | Generator rule from a cycle counter or calendar | ⚠️ C3 |
| UC-09 | Utility meter readings | Monthly generator rule, external deadline (R2, level 2), sending on the user's behalf with approval. The amount for the budget overlaps with Fulla | ⚠️ C3, C7 |
| UC-10 | Family chore coordination | The flow assumes one user. Whose quadrant, who executes, who approves — undefined | ❌ |
| UC-11 | Seasonal home preparation | Generator rule → SMART goal with a checklist of steps | ⚠️ C3 |

### Fulla — personal administration

| ID | Scenario | Path through the stages | Result |
|---|---|---|---|
| SEC-UC-01 | Pay an invoice | Clarify → SMART task (+ the document as a reference) → slot before the deadline. The "move to payday" button is **the best test of R2**: the deadline (level 2) beats convenience and yields only to an explicit user decision (level 3). Works as intended | ✅ |
| SEC-UC-02 | Send documents | Clarify sees gaps in S and A → one question → SMART goal with two steps → slots with contexts "home" and "on the way" → stamp purchase with approval → waiting-for | ✅ |
| SEC-UC-03 | Backward time-blocking | The Slot planner (stage 5) cuts the task into four steps itself. Splitting into steps is formulation (stage 3): breaks R1 | ⚠️ C5 |
| SEC-UC-04 | Five-minute micro-step | Review rewrites the formulation S ("take out the folder") and sets a fixed slot. Both fields belong to other stages: breaks R1 | ⚠️ C5, C6 |
| SEC-UC-05 | Admin hour | Stage 5 groups tasks by energy "routine" and duration | ✅ |
| SEC-UC-06 | Auto-rescheduler | "Compress the task" changes its duration, a formulation field: breaks R1 | ⚠️ C5 |
| SEC-UC-07 | Waiting-for tracker | "Waiting" is set by Engage, "graveyard" by Review: the status has two writers. The rest works | ⚠️ C6 |
| SEC-UC-08 | Kündigungsfrist guardian | Deadline from the contract (level 2), template, sending with approval. Overlaps with Hrimfaxi UC-05 | ⚠️ C7 |
| SEC-UC-09 | Pre-start briefing | Read-only at stage 5 | ✅ |
| SEC-UC-10 | Energy and overbooking guard | Stage 5 checks the 80% limit and energy | ✅ |
| SEC-UC-11 | Event preparation | The calendar creates the input → SMART task 5–7 days ahead | ✅ |
| SEC-UC-12 | Weekly review | This is stage 6 itself | ✅ |

### Totals

| Agent | ✅ | ⚠️ | ❌ |
|---|---|---|---|
| Hrimfaxi (10) | 2 | 8 | 0 |
| Frigg (11) | 2 | 8 | 1 |
| Fulla (12) | 7 | 5 | 0 |
| **All (33)** | **11** | **21** | **1** |

Fulla passes best because its scenarios were already written around the SMART passport. Hrimfaxi and Frigg break the flow in the same places, which points to gaps in the flow, not in the scenarios.

---

## 3. Eight flow changes

| # | Problem | Change | Cases |
|---|---|---|---|
| **C1** | The flow assumes the user enters something. Questions ("what does the car cost me", "towing number", "what does E18 mean") create nothing | At stage 1, fork **query vs input**. A query is answered from references at once and does not enter the flow | H-05, H-09, H-10, F-07 |
| **C2** | Clarify chooses "reference **or** SMART goal". An invoice, a service order or squeaking brakes yield several objects at once, and sometimes an answer is needed right now | Clarify **splits an input into parts**: each part is a reference or a SMART goal, and an immediate answer is allowed (GTD two-minute rule). **Applied in this PR:** [PRINCIPLES.md](./PRINCIPLES.md) §8, [GLOSSARY.md](./GLOSSARY.md), REQ-L07 | H-01, H-02, H-03, F-06 |
| **C3** | Recurring work (service, tires, cleaning, filters, meters, seasons) comes from a schedule, not the user. It is neither a habit nor a one-off goal | New track **Recurring rules** (RU: *регламенты*): a generator rule with a template creates an already-clarified SMART task that enters at stage 3. The next due date counts from actual completion | H-06, H-07, F-03, F-04, F-08, F-09, F-11 |
| **C4** | Shopping-list entries and context-only tasks do not need SMART criteria or an Eisenhower quadrant | **Light path**: a list entry is a line inside a SMART task "buy from the list" with the context "in the shop"; stage 4 is skipped | F-01, F-02, F-03 |
| **C5** | Stages 5 and 6 want to change the formulation: split into steps, shrink the duration, invent a micro-step | Explicit **back transition "return to formulation"**: stage 5/6 proposes, stage 3 writes, the user confirms | SEC-03, SEC-04, SEC-06 |
| **C6** | Several stages change the lifecycle status (Engage: done, waiting; Review: graveyard, someday). This contradicts R1 — version 1 of the flow stated it imprecisely | The status has **one owner** — the lifecycle module (Tasks). Stages send it events. A domain incident status (Hrimfaxi) maps to the SMART goal status through a mapping table: the domain reports "artifact M arrived", the platform closes the goal | H-01, SEC-04, SEC-07 |
| **C7** | One contract or invoice can create tasks in two agents (insurance: renewal in Hrimfaxi and cancellation in Fulla; repair invoice; Stadtwerke) | **One obligation — one object.** Clarify routes: data stays with the domain, the obligation "pay / cancel / renew" goes to Fulla. Deduplication by document. Same rule as proposed in [SECRETARY_USER_CASES.md](./SECRETARY_USER_CASES.md) §6 | H-03, H-05, F-09, SEC-08 |
| **C8** | R3 says "quadrant at the weekly review", but urgent items (brakes, sofa) cannot wait until Friday | The quadrant is set **provisionally on arrival** and confirmed at review. For dangerous subsystems the safety rule sets it, not an agent proposal (matches the 🔴 safety-rule task in [TODO.md](./TODO.md)) | H-01, H-02, F-06 |

---

## 4. Flow after the changes (version 2, proposed)

```
                  Safety — fires before any stage
                                  │
   Query ───────▶ answered at once from references (does not enter the flow)
                                  │
   Input ──▶ 1. Capture ─▶ 2. Clarify ─┬─▶ reference
                          (splits into  ├─▶ immediate answer
                           parts)       └─▶ SMART goal ─┐
                                                        ▼
   Recurring rule (generator) ────────────▶ 3. Formulate ◀──────────┐
                                                 │                  │ return to
                                    ┌────────────┴─────────┐        │ formulation
                                    ▼                      ▼        │
                            4. Prioritize            light path     │
                            provisional on arrival,  (lists,        │
                            confirmed at review      context only)  │
                                    └────────┬─────────────┘        │
                                             ▼                      │
   Habits (own track, reserved in the 80%) ─▶ 5. Engage ────────────┤
                                             ▼                      │
                                        6. Review ──────────────────┘
                                             │
             lifecycle status is written only by the Tasks module (from stage events)
```

Only C2 is applied to the rule documents in this PR. C1 and C3–C8 are recorded as open tasks in [TODO.md](./TODO.md).

---

## 5. Still open

- **❌ Frigg UC-10 and households in general.** The flow is single-user. It needs the decision "single user vs household" from [TODO.md](./TODO.md): who owns a task, whose quadrant, who approves. Candidate method: *Fair Play* (Eve Rodsky) — each task has one owner end to end.
- **Long-term goals are untested.** No scenario is a level-3 goal ([SMART_GOALS.md](./SMART_GOALS.md) §13), so WOOP, lead / lag, key results and areas of focus have no evidence yet (section 7).
- **Habits are untested.** No scenario in the catalogs covers habits (Duhigg habit loop, Clear's system of small changes), so R4 has no evidence yet. Two or three habit scenarios are needed.
- **Eisenhower without the bottom row.** In [SMART_GOALS.md](./SMART_GOALS.md) §3 the "not important" quadrants are "to be defined", yet several cases (discounts, small seasonal items) need exactly them.
- **Status mapping table** between Hrimfaxi incidents and SMART goals is not written yet (C6 and P0 in [HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md)).

## 6. What held up

- **Precedence (R2)** worked in the sharpest places: brakes (level 1), the "move to payday" button in SEC-UC-01 (level 2 against level 3), purchases and sending letters (level 1 — approval).
- **Stage 5** fits the admin hour, the energy guard, the briefing and the contexts "home / on the way" without strain.
- **R5 "the domain supplies facts"** separates the two state machines in UC-01. This is the direction for resolving the `active_tracking` P0 in [HRIMFAXI_CASE_REVIEW.md](./HRIMFAXI_CASE_REVIEW.md).

---

## 7. Second run — SMART practices and depth levels

> Checked on 2026-10-16 against [SMART_GOALS.md](./SMART_GOALS.md) Part 4: practices per criterion (next action, definition of done, lead / lag, WOOP, responsible / accountable, areas of focus, hard vs soft deadline, backcasting) and depth levels 0–3 with a question budget.

Legend: ✅ practices fit · ➖ not applicable (reference, query or list entry — no SMART passport) · ⚠️ led to a refinement of Part 4 · ❌ blocked.

### Hrimfaxi — vehicle

| ID | Level | What the practices produce | Result |
|---|---|---|---|
| UC-01 Brakes | 2 | Next action "book a diagnosis"; definition of done = invoice uploaded or repair confirmed (already in the scenario's closing step). The one question in the scenario fits the budget; safety reaction comes before it | ✅ |
| UC-02 Check Engine | 2 | As UC-01; the immediate checklist is an answer, not a question | ✅ |
| UC-03 Service invoice | 1 | Payment task: done = transfer confirmation. Mechanic's recommendation "rear pads 20%": no hard deadline → **review date** instead of an invented deadline | ✅ |
| UC-04 Fuel receipt | — | Reference | ➖ |
| UC-05 Insurance / TÜV | 1 | Renewal: hard deadline from the document, done = new policy or inspection report | ✅ |
| UC-06 Scheduled service | 2 | Created by a recurring rule with a template: next action "book the garage", done = invoice uploaded. 0 questions | ✅ |
| UC-07 Tire swap | 2 | Definition of done as a checklist: tires swapped, storage location recorded, tread depth noted | ✅ |
| UC-08 Part research | 1 | Done = user picked an option or cart prepared; purchase stays behind approval | ✅ |
| UC-09 Cost of ownership | — | Query. Note: it reads a **lag measure**; a future level-3 goal "lower car costs" would use it | ➖ |
| UC-10 Service passport | — | Query + export | ➖ |

### Frigg — home

| ID | Level | What the practices produce | Result |
|---|---|---|---|
| UC-01 Discounts | 0 | List entry, light path | ➖ |
| UC-02 Photo → list | 0 | List entry, light path | ➖ |
| UC-03 Pantry low stock | 0 | List entry from a recurring rule | ➖ |
| UC-04 Floating cleaning | 1 | Recurring rule, done = "bed linen changed". Each run is a **lead measure** of the area "home in order" | ✅ |
| UC-05 Loose handle | 1 | Verb with a finish: "fix the cabinet handle". The scenario asks for the lamp / socket type — a **blocking prerequisite**, so level 1 cannot be "0 questions" strictly. Refinement: level 1 allows one question for a blocking gap | ⚠️ |
| UC-06 Dog and sofa | 2 | Next action = the first-aid steps already given; done = "stain and smell removed", confirmed at the 24-hour check. One question (which branch) fits the budget; upholstery comes from the passport, not a question | ✅ |
| UC-07 Appliance passport | — | Reference | ➖ |
| UC-08 Appliance care | 1 | Recurring rule; the prerequisite (descaler in the pantry) is checked automatically, not asked | ✅ |
| UC-09 Meter readings | 1 | Recurring rule, hard deadline, done = "readings submitted" | ✅ |
| UC-10 Family coordination | 2 | **Responsible / accountable** gives the model: one person shops, one owns the list. Still blocked by the household decision (permissions, location privacy) | ❌ |
| UC-11 Seasonal home care | 2 | Ideal case for a definition-of-done checklist; next action = first checklist item | ✅ |

### Fulla — personal administration

| ID | Level | What the practices produce | Result |
|---|---|---|---|
| SEC-UC-01 Pay an invoice | 1 | The SMART passport already has the completion artifact (= definition of done) and a perfective verb | ✅ |
| SEC-UC-02 Send documents | 2 | Next action "print and sign"; exactly one question — the budget of level 2 | ✅ |
| SEC-UC-03 Backward time-blocking | 2 | Backcasting milestones were listed only for level 3, but this level-2 goal needs them. Refinement: **attributes trigger practices** (hard deadline + several slots → milestones), the level only sets the question budget | ⚠️ |
| SEC-UC-04 Micro-step | 2 | The five-minute micro-step **is** a smaller next action. "5 whys" fits here as an optional ladder step before the graveyard | ✅ |
| SEC-UC-05 Admin hour | — | Stage 5 only | ➖ |
| SEC-UC-06 Rescheduling | — | Stage 5 only | ➖ |
| SEC-UC-07 Waiting-for | 1 | Done = "reply received" | ✅ |
| SEC-UC-08 Kündigungsfrist | 2 | Next action "send the Kündigung"; done = Kündigungsbestätigung (already in the passport); hard deadline from the contract | ✅ |
| SEC-UC-09 Briefing | — | Read-only | ➖ |
| SEC-UC-10 Energy guard | — | Confirms that capacity planning belongs to stage 5, not to A | ✅ |
| SEC-UC-11 Event preparation | 1 | Budget 30 € in M; backcasting from the event date | ✅ |
| SEC-UC-12 Weekly review | — | This is the weekly sprint; "5 whys" fits the "stalled" block | ✅ |

### Totals of the second run

| Agent | ✅ | ➖ | ⚠️ | ❌ |
|---|---|---|---|---|
| Hrimfaxi (10) | 7 | 3 | 0 | 0 |
| Frigg (11) | 5 | 4 | 1 | 1 |
| Fulla (12) | 8 | 3 | 1 | 0 |
| **All (33)** | **20** | **10** | **2** | **1** |

### Findings

1. **Level 0 is needed.** List entries (Frigg UC-01–03) do not carry a SMART passport; this matches the light path (C4).
2. **Attributes trigger practices; the level sets the question budget** (SEC-UC-03).
3. **Level 1 may ask one question for a blocking prerequisite** (Frigg UC-05).
4. **Placement holds:** Eisenhower stays in stage 4, capacity in stage 5 (SEC-UC-10), "5 whys" only at review for stalled goals (SEC-UC-04, SEC-UC-12).
5. **Definition of done already exists** in most scenarios as the closing condition or the completion artifact; the practice formalizes it rather than adding work.
6. **No level-3 goal in any catalog.** WOOP, lead / lag, key results and areas of focus are untested, like the habits track. Long-term goal scenarios are needed (e.g. a savings goal, a renovation, learning a language).

Refinements 1–3 are already written into [SMART_GOALS.md](./SMART_GOALS.md) §13.
