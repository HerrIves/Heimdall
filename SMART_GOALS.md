# Heimdall — SMART Goals: Lifecycle, Review and Contexts

> **Status: draft product ideas.** This document collects ideas for how SMART goals live, get reviewed, and find the right moment to be done. These are directions for development, not final principles. Active rules stay in [PRINCIPLES.md](./PRINCIPLES.md); terms are defined in [GLOSSARY.md](./GLOSSARY.md).
>
> It extends [PRINCIPLES.md](./PRINCIPLES.md) §8 and REQ-L07–L09 in [REQUIREMENTS.md](./REQUIREMENTS.md): every input is classified as a reference or a SMART goal. This document describes what happens to a SMART goal after that.

A SMART goal has two independent axes:

| Axis | Question it answers | Examples |
|---|---|---|
| **Time** | *When* should it be done, and how much does it matter? | deadline, urgency, importance, review frequency |
| **Context** | *Where and under which conditions* can it be done at all? | place, available free time, tools needed |

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

## Related scenarios

These ideas already appear in the agent scenario catalogs:

| Idea | Scenario |
|---|---|
| Observation becomes a SMART goal | Hrimfaxi UC-01 "brakes squeak" ([HRIMFAXI_USER_CASES.md](./HRIMFAXI_USER_CASES.md)); Frigg UC-05 "loose cabinet handle" ([HOME_USER_CASES.md](./HOME_USER_CASES.md)) |
| Postponing without losing the goal; next interval counted from actual completion | Frigg UC-04 floating cleaning intervals |
| Follow-up until verified completion | Hrimfaxi UC-01, UC-06; [CAR_AGENT.md](./CAR_AGENT.md) §3 |
| Context of place and available time | Frigg UC-10 family coordination (location context); shopping lists in Frigg UC-01–UC-02 |

---

## Open questions

- Who owns lifecycle states — the Tasks module or the domain agent?
- How strong should escalation be for long-postponed goals, and where does it stop being helpful?
- Exact values: the threshold **N**, and the review frequencies per quadrant.
- How tasks inherit context from their SMART goal, and whether context belongs to the goal or to each task.
- Security and privacy of context signals: location and NFC events reveal where the user is ([PRINCIPLES.md](./PRINCIPLES.md) §12, §22).
