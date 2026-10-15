# Heimdall — Glossary

> Shared vocabulary for Heimdall's documents, discussions, and code. When a term here conflicts with older wording (for example in the frozen `brainstorm.md`), this glossary wins.
>
> Rules live in [PRINCIPLES.md](./PRINCIPLES.md); this file only defines what words mean.

## The word "project"

"Project" was used for three different things. From now on each meaning has its own term:

| Meaning | Term to use | Example |
|---|---|---|
| (a) Heimdall itself as a product / this repository | **Heimdall** or **the repository** | "Set up the repository structure." |
| (b) The managed work object that an actionable note turns into | **SMART goal** (RU: *SMART-цель*) | "The wheel squeaks" → SMART goal *"Squeak diagnosed and fixed"* |
| (c) A possible future domain agent for personal projects | **Project Agent** (always with "Agent") | "The second domain agent could be the Project Agent." |

Avoid the bare word "project" in specifications. Older documents that say "project / work item" in sense (b) should be read as **SMART goal**. The word "project" is deliberately not used for this object, so it is never confused with the Project Agent.

## Information and work

| Term | Meaning |
|---|---|
| **Note** | Raw captured input — text, voice, photo, document — before Heimdall has classified it. A note is a starting point, not a place where information stays. |
| **Item** | Any object Heimdall manages after classification. Umbrella term; every item has a type and a lifecycle state. |
| **Reference** | An item intentionally kept as information only: a record, a document, a fact, an idea without current action intent. |
| **SMART goal** (RU: *SMART-цель*) | An actionable item with a clearly defined desired result, shaped by the SMART criteria — Specific, Measurable, Achievable, Relevant, Time-bound — where they help. Tracked until achieved, cancelled, or explicitly closed ([PRINCIPLES.md](./PRINCIPLES.md) §8). Usually contains tasks. |
| **Task** | A concrete action step toward a SMART goal (or a standalone small action). May have a deadline, a trigger, and someone responsible for it. |

## Classification rule

Every input must be deliberately classified as either a **reference** or a **SMART goal**. An input left hanging as a passive, undecided note is not allowed. This rule applies across all domains — vehicle (Hrimfaxi), home (Frigg), finance, and future agents.

Not every input becomes a SMART goal: purely informational data (a VIN, a photo of a document, a note to remember) stays a reference. What matters is that this is a conscious choice, not an accidental dead end. Full rule: [PRINCIPLES.md](./PRINCIPLES.md) §8.

```
note ──▶ classification ──┬──▶ reference   (kept as information)
                          └──▶ SMART goal  ──▶ tasks ──▶ achieved / cancelled / closed
```

Lifecycle states of SMART goals (active, waiting, achieved, cancelled, someday/maybe, goal graveyard) are drafted in [SMART_GOALS.md](./SMART_GOALS.md); requirements REQ-L07–L09 in [REQUIREMENTS.md](./REQUIREMENTS.md).

## System components

| Term | Meaning |
|---|---|
| **Heimdall / Orchestrator** | The central component that receives requests and events, routes them to the responsible agent, and coordinates results. "Heimdall" is reserved for it. |
| **Agent** (domain agent) | Owns a complete area of responsibility end to end — its decisions, workflows, and domain data. Examples: **Hrimfaxi** (vehicle), **Frigg** (home, candidate), Finance agent. |
| **Module** | A reusable technical capability used by several agents, e.g. Tasks, Scheduler, Notifications, Documents, OCR, Budget, Shopping, Search, Context provider. A module is not an agent, even if it uses an LLM ([PRINCIPLES.md](./PRINCIPLES.md) §5). |
| **Integration** | A connection to an external service: calendar, shop, payment provider, external API. |
| **Channel / Interface** | A way the user talks to Heimdall: mobile app, Telegram, voice. Channels contain presentation logic only, no business logic ([PRINCIPLES.md](./PRINCIPLES.md) §3). |
| **Event** | A record that something happened — "invoice recorded", "deadline reached". Events are delivered by deterministic infrastructure and let components react without being hard-wired to each other. |

## Naming

Norse mythology names ([PRINCIPLES.md](./PRINCIPLES.md) §24) with their meaning:

| Name | Component | Status | Why it fits |
|---|---|---|---|
| **Heimdall** | Central orchestrator | Agreed | Watchman of the gods: observes, notices early, raises the alarm |
| **Hrimfaxi** (Hrímfaxi) | First domain agent — vehicle ownership and maintenance. Descriptive alias: **Car Agent** | Agreed | The tireless horse that draws Night across the sky: endurance and continuous care for the user's vehicles |
| **Frigg** | Home / household agent | Candidate | Queen of Asgard, guardian of the hearth, household order and foresight |

The word "vehicle" describes the *domain*; the agent itself is called Hrimfaxi.
