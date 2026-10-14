# Heimdall

Modular, proactive personal assistant platform.

## Principles
- Runs continuously; scheduled workflows work independently of LLM availability.
- Provider-agnostic LLM gateway with configurable models.
- Orchestrator routes requests to predefined domain agents; it does not generate agents or modules at runtime.
- Domain agents own end-to-end workflows and domain data.
- Reusable modules provide tasks, scheduling, documents/OCR, budgets, notifications and approval-gated payments.
- External actions with financial consequences require explicit user approval.

## First domain agent: Vehicle
Track vehicle details, maintenance, expenses, parts, documents and upcoming deadlines.

## Status
Architecture brainstorming; implementation and technology decisions pending.
