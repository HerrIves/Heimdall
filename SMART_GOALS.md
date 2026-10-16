# Heimdall — SMART Goals: Lifecycle, Review, Contexts and Load

> **Status: draft product ideas.** This document collects ideas for how SMART goals live, get reviewed, and find the right moment to be done. These are directions for development, not final principles. Active rules stay in [PRINCIPLES.md](./PRINCIPLES.md); terms are defined in [GLOSSARY.md](./GLOSSARY.md).
>
> It extends [PRINCIPLES.md](./PRINCIPLES.md) §8 and REQ-L07–L09 in [REQUIREMENTS.md](./REQUIREMENTS.md): every input is classified as a reference or a SMART goal. This document describes what happens to a SMART goal after that.

A SMART goal (and each of its tasks) has three independent axes:

| Axis | Question it answers | Examples |
|---|---|---|
| **Time** | *When* should it be done, and how much does it matter? | deadline, slot, urgency, importance, review frequency |
| **Context** | *Where and under which conditions* can it be done at all? | place, available free time, tools needed |
| **Energy** | *How much effort* does it take, and of which kind? | duration; energy index: high focus / routine / physical trip (Part 3) |

### Time (the "T" in SMART) and context are separate axes

The "T" covers **time only**:

- **Hard deadline** — the latest date by which it must be done. **Optional**: many tasks have none.
- **Scheduled slot** — concrete time in the calendar, used when the task needs one; proposed by the Slot planner and confirmed by the user.

**Place context is not part of T.** It is its own axis (Part 2) and a **second way to trigger a task**, alongside time:

```
        TIME  (T)                                 CONTEXT  (separate axis)
  deadline — optional                        place, free time, tools
  slot     — when a fixed time is needed     "in the shop", "at my desk"
            │                                          │
            ▼                                          ▼
   triggered by time                          triggered by context
   "Fri 23.10, 18:30"                         "the user is in the shop"
```

| Example | Deadline | Slot | Context | Triggered by |
|---|---|---|---|---|
| Pay the Stadtwerke bill | 28.10 | Fri 23.10, 18:30 | — | time |
| Buy milk | none | none | in the shop | **context trigger** — offered when the user is in the shop |
| Buy a present by Saturday | Sat | none | in the shop | context; a time reminder as the deadline approaches |

---

## Part 1 — Lifecycle and review

### 1. Lifecycle states

```
note ──▶ classification ──┬──▶ reference
                          │
                          └──▶ SMART goal
                                   │
                         ┌─────────┴─────────┐
                         ▼                   │
                      active  ◀──────▶   waiting
                         │
          ┌──────────────┼───────────────┬──────────────────┐
          ▼              ▼               ▼                  ▼
      achieved      cancelled     someday / maybe     goal graveyard
                                   (not active,        (archived, frozen,
                                    resurfaces          never deleted;
                                    periodically)       can be revived)
```

- **active** — being worked on.
- **waiting** — blocked on someone or something (a garage appointment, a delivery).
- **achieved** / **cancelled** — terminal states.
- **someday / maybe** — not urgent, not active, deliberately parked (GTD "someday/maybe"). Does not clutter the active view but resurfaces on a slow schedule.
- **goal graveyard** — an archive for goals that were postponed for a long time. Nothing is deleted: a goal can be revived from the graveyard at any time.

### 2. Regular review (the "reflect" step)

Classification alone does not prevent goals from dying quietly: a SMART goal such as "replace the brake pads" can still hang for weeks. Heimdall therefore runs a **regular review** — the "reflect" step of GTD, which is the one most often forgotten.

- The review is **deterministic**: it runs on a schedule kept by infrastructure, not "when the model remembers" ([PRINCIPLES.md](./PRINCIPLES.md) §10).
- The LLM only phrases the question at review time, e.g. *"The brake pads goal has been open for two weeks — do it, postpone it, or close it?"*

### 3. Priority by the Eisenhower matrix → review frequency

Each SMART goal is placed in a quadrant of the Eisenhower matrix (important / urgent). The quadrant and the presence of a deadline determine how often the goal is reviewed.

| | **Urgent** | **Not urgent** |
|---|---|---|
| **Important** | frequent review, up to daily | weekly review |
| **Not important** | to be defined | to be defined |

| Situation | Review rhythm (indicative) |
|---|---|
| Urgent goal with a deadline | often — up to daily (e.g. "review tonight") |
| Important, not urgent | weekly |
| No deadline, or a deadline cannot be set yet | rare background review — monthly or quarterly |
| someday / maybe | quarterly |
| goal graveyard | about every six months |

**Human-in-the-loop:** the agent *proposes* the quadrant; the user *confirms* it.

### 4. Long-postponed goals without a deadline

- Goals are **never deleted** just because they keep being postponed.
- After a goal has been postponed **N** times, Heimdall gently offers to move it to the **goal graveyard** — helping the user let go honestly, without pressure and without losing anything.
- Non-urgent goals can go to **someday / maybe** instead of staying active.
- About every six months Heimdall looks through the graveyard and asks whether anything has become relevant again.

---

## Part 2 — Execution contexts

### 5. Context as a second axis

Besides time, a SMART goal (or its tasks) has an **execution context**: where and under which conditions it can be done.

- **place** — shop, desk / computer, car, home;
- **available free time** — e.g. 20 minutes;
- **tools / prerequisites** — e.g. needs a laptop, needs the car.

"Buy a cabin filter" only makes sense in a shop; "sort out the desk" only at home. This is GTD contexts in an extended form.

### 6. Reversed interaction: the task finds the user

The user does not only ask Heimdall what to do. The user **announces a context**, and Heimdall answers with the SMART goals and tasks that are doable *here and now*:

- "I'm at my desk."
- "I'm in the shop, 20 minutes free."
- "I have some free time." → no place given: Heimdall asks, or suggests across all contexts.

This is especially useful for things the user wants to capture now but do later, when the right place or free time comes up.

### 7. Three ways to set the context

| Source | Precision | Notes |
|---|---|---|
| **Voice / text** — "I'm at my desk" | exact, explicit | always available |
| **Geolocation** | coarse — good for large places (home, a shop) | cannot tell desk from kitchen |
| **NFC tag** | precise — a specific point (desk, car) | a deliberate, deterministic signal of intent: touching the tag means "I'm here and ready" |

NFC fits the existing principles: a simple event-driven trigger instead of continuous GPS polling ([PRINCIPLES.md](./PRINCIPLES.md) §18, §21).

### 8. An NFC tag as a shared "I'm here" event

One touch of the phone produces one event on the event bus; several consumers subscribe to it.

```
phone touches NFC tag in the car
              │
              ▼
     event: "user is in the car"
              │
     ┌────────┴────────┐
     ▼                 ▼
 phone navigation   Heimdall / Hrimfaxi
 set up for the     picks up the context
 trip               (e.g. relevant car tasks)
```

One event — several reactions, without hard-wiring consumers to each other.

### 9. Context provider module

A reusable **context provider** module is emerging: it collects signals about place and available time (voice, geolocation, NFC) and publishes **context events** that agents can subscribe to. It is a module, not an agent ([PRINCIPLES.md](./PRINCIPLES.md) §5).

---

## Part 3 — Energy and load

### 10. Energy index as a third axis

Besides *when* and *where*, a task has a **duration** and an **energy index** (RU: *индекс энергии*):

| Energy index | RU | Examples |
|---|---|---|
| 🧠 **High focus** | Высокий фокус | report, tax return, comparing offers |
| 🔁 **Routine** | Рутина | paying bills, short calls, forms |
| 🚗 **Physical trip** | Физический выезд | post office, garage, shop |

**Purpose:**

- do not schedule several heavy (high-focus) tasks in a row, e.g. after a working day;
- do not overload a day or a weekend;
- combine with contexts: routine tasks go into an admin hour, trips are grouped by route.

### 11. Load rule — the attention budget

**No more than 80% of the user's free time is filled with planned tasks.** When a new task would exceed this, the Slot planner does not add it silently; it shows the load and asks what to move:

> "Saturday already has 5 hours of focused work and 2 trips. If we add this, a deadline will slip. What shall we move to Tuesday?"

This closes the open gap **"attention budget"**. The 80% value is a starting point, not a fixed rule.

**Origin:** the secretary scenario SEC-UC-10 "Resource & Energy Guard" ([SECRETARY_USER_CASES.md](./SECRETARY_USER_CASES.md)). It builds on David Allen's GTD practice of choosing the next action not only by context and available time, but also by available energy.

---

## Part 4 — Practices per SMART criterion and depth levels

Each SMART criterion is backed by an established practice, so the assistant asks the right guiding question and can check a goal deterministically instead of treating SMART as a dry checklist. The practices are placed on the stages of the shared flow (capture → clarify → formulate → prioritize → engage → review, see [FLOW_CASE_REVIEW.md](./FLOW_CASE_REVIEW.md)), so that each field still has exactly one writer.

### 12. Practices per criterion

| Criterion | Practice | Stage | What it adds to the SMART goal | Source |
|---|---|---|---|---|
| **S** Specific | **Next action** — a goal is not specific until its first visible physical step is defined | 3 Formulate | `next_action` | GTD (David Allen) |
| **S** | Wording as a **verb with a clear finish** — "paint the nursery walls", not "work on the renovation" (RU: perfective infinitive, *покрасить*, which also satisfies the "infinitive" rule of the SMART passport in [SECRETARY_USER_CASES.md](./SECRETARY_USER_CASES.md) §2) | 3 Formulate | title | — |
| **S** | **5W** (what, why, who, where, which) — only for the gaps that are actually missing | 3 Formulate | — | — |
| **M** Measurable | **Definition of done** — a binary checklist when the result cannot be counted ("winter-ready car: tires swapped, washer fluid, battery checked"). Same as the *completion artifact* of the SMART passport | 3 Formulate | `definition_of_done` | Agile |
| **M** | **Lead and lag measures** — the lag measure is the end result ("save 5,000 €"), the lead measure is the regular action that drives it ("put aside 150 € a week"). A lead measure is a recurring rule or a habit, so it links a goal to those tracks | 3 Formulate | `lag`, `lead` → recurring rule / habit | *The 4 Disciplines of Execution* (McChesney, Covey, Huling) |
| **M** | **Key results** — "I will achieve X as measured by 2–3 key results"; only for long-term goals | 3 Formulate | key results | OKR (John Doerr, *Measure What Matters*) |
| **A** Achievable / assignable | **WOOP** — wish, outcome, obstacle, plan in the form "if X happens, I will do Y" | 3 Formulate | `if_then_plans` | Gabriele Oettingen; implementation intentions (Peter Gollwitzer) |
| **A** | **Responsible + accountable** — exactly one person does the task, exactly one accepts the result (RACI reduced to R and A for a household) | 3 Formulate | `responsible`, `accountable` | RACI |
| **R** Relevant | **Areas of focus** — which life area (family, health, finance, home, car, work) or 1–3-year goal the goal serves. No area → offer *someday / maybe* | 2 Clarify | `area` | GTD horizons of focus |
| **T** Time-bound | **Hard vs soft deadline** — only hard commitments get a deadline; the rest get a **review date** instead of an invented deadline | 3 Formulate (deadline), 6 Review (review date) | `deadline` optional, `next_review` | GTD |
| **T** | **Backcasting** — milestones planned backwards from a fixed date | 5 Engage proposes, 3 Formulate writes | milestones | — |
| **T** | **Weekly sprint** — the weekly review picks which goals get time this week | 6 Review | — | Scrum; *The 12 Week Year* (Brian Moran) |

**Placement rules — what deliberately does not belong to a criterion:**

- **Eisenhower and Pareto are not part of R.** Relevance only answers "which area does this serve?". The quadrant is written by stage 4 (Prioritize).
- **Capacity planning is not part of A.** Overload is visible only when slots are planned, so the check lives in stage 5 (the 80% rule, §11). A proposal to reduce scope goes back to stage 3 (*return to formulation*).
- **"5 whys" is not asked at creation.** It conflicts with "ask only for useful missing information" ([PRINCIPLES.md](./PRINCIPLES.md) §9). It is used only at review for a **stalled** goal, as an optional step of the postponement ladder before the goal graveyard.

### 13. Depth levels and question budget

Applying every practice to every goal turns the assistant into a questionnaire. The depth depends on the size of the item:

| Level | Item | Practices applied | Questions to the user |
|---|---|---|---|
| **0** | List entry, context-only item (light path) | none | 0 |
| **1** | SMART task — one step | verb with a finish, definition of done | 0, unless a **blocking prerequisite** is missing (then 1) |
| **2** | SMART goal — several steps | + next action, responsible / accountable | at most 1 |
| **3** | Long-term goal — weeks or longer | + WOOP, lead / lag, key results, area of focus, milestones | 2–3, spread over several reviews |

Rules:

1. **The level sets the question budget; attributes trigger practices.** A practice is applied whenever its trigger is present, whatever the level: a hard deadline plus several slots → backcasting milestones, even at level 2.
2. **Defaults before questions.** Whatever can be derived (definition of done from a template, area from the domain agent, responsible person when there is a single user) is filled in by the assistant and shown for confirmation, not asked.
3. **The area defaults to the domain agent** (Hrimfaxi → car, Frigg → home, Fulla → administration). It is asked only for level 3 or when the item crosses domains.
4. **Safety first.** For a safety case no S/M/A question is asked before the safety reaction ([FLOW_CASE_REVIEW.md](./FLOW_CASE_REVIEW.md), rule R2).

### 14. Scenario check

All 33 scenarios were run against this part: [FLOW_CASE_REVIEW.md](./FLOW_CASE_REVIEW.md) §7. Result: the practices fit 20 scenarios, 10 do not use SMART practices at all (references, queries, list entries), 2 led to the refinements above (rules 1 and the level-1 exception), 1 remains blocked (household). **No current scenario is a level-3 goal**, so WOOP, lead / lag, key results and areas of focus are not yet checked against any case.

---

## Related scenarios

These ideas already appear in the agent scenario catalogs:

| Idea | Scenario |
|---|---|
| Observation becomes a SMART goal | Hrimfaxi UC-01 "brakes squeak" ([HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md)); Frigg UC-05 "loose cabinet handle" ([HOME_USER_CASES.md](./HOME_USER_CASES.md)) |
| Postponing without losing the goal; next interval counted from actual completion | Frigg UC-04 floating cleaning intervals |
| Follow-up until verified completion | Hrimfaxi UC-01, UC-06; [CAR_AGENT.md](./CAR_AGENT.md) §3 |
| Context of place and available time | Frigg UC-10 family coordination (location context); shopping lists in Frigg UC-01–UC-02 |
| Slots, admin hour, rescheduling, weekly review, waiting-for, briefing | Fulla SEC-UC-03–07, 09, 11, 12 ([SECRETARY_USER_CASES.md](./SECRETARY_USER_CASES.md)) |
| Energy index and load rule | Fulla SEC-UC-10 |

All 33 scenarios were run through the stage flow built on this document (capture → clarify → formulate → prioritize → engage → review): [FLOW_CASE_REVIEW.md](./FLOW_CASE_REVIEW.md). Several open questions below are answered there as proposals (C6 lifecycle-status owner, C8 provisional quadrant, C5 return to formulation).

---

## Open questions

- Which life areas (areas of focus, §12) does Heimdall use, and are they the same as the domain agents?
- Where are lead measures stored: as recurring rules, as habits, or as both?
- Who owns lifecycle states — the Tasks module or the domain agent?
- How strong should escalation be for long-postponed goals, and where does it stop being helpful?
- Exact values: the threshold **N**, and the review frequencies per quadrant.
- How tasks inherit context from their SMART goal, and whether context belongs to the goal or to each task.
- Who sets the energy index and duration: proposed by the agent and confirmed by the user, or learned from completed tasks?
- Is 80% the right load threshold, and should it differ between weekdays and weekends?
- Security and privacy of context signals: location and NFC events reveal where the user is ([PRINCIPLES.md](./PRINCIPLES.md) §12, §22).
