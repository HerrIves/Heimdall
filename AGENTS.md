# AGENTS.md — Working in the Heimdall repository

> **Open tasks: [TODO.md](./TODO.md).** Read it before starting work.
>
> This file is for coding assistants and contributors working on this repository. It does not describe Heimdall's product agents (Hrimfaxi, Frigg, Fulla) — those are in [GLOSSARY.md](./GLOSSARY.md) and the agent documents.

## Start of a session

1. Read [README.md](./README.md) — map of the documents.
2. Read [PROGRESS.md](./PROGRESS.md) — current phase and the next concrete step.
3. Check [TODO.md](./TODO.md) — open tasks, ordered by importance.
4. Before designing a component, apply the checklist in [PRINCIPLES.md](./PRINCIPLES.md); use the terms from [GLOSSARY.md](./GLOSSARY.md).

## Rules

| Topic | Rule |
|---|---|
| **Open tasks** | Live in [TODO.md](./TODO.md). When a PR closes a task, tick it there in the same PR with the PR number. New open tasks go there, not into other documents. |
| **Project status** | Kept **only** in [PROGRESS.md](./PROGRESS.md). Other documents link to it instead of restating the phase or the next step. |
| **Language** | Target language for repository documents is **English**. Russian terms may be added in parentheses (e.g. *SMART goal (RU: SMART-цель)*). Exceptions: documents the owner explicitly keeps in Russian as her own working notes (currently [PROGRESS.md](./PROGRESS.md) and [SECRETARY_USER_CASES.md](./SECRETARY_USER_CASES.md)). Do not mix languages within one paragraph; do not translate existing documents unless a task asks for it. |
| **Changes** | Every change goes through a **branch and a pull request**. Never push directly to `main`. Only the repository owner merges. |
| **Pull requests** | Fill in the [PR template](./.github/pull_request_template.md): the security sections (*Security impact*, *Untrusted inputs and trust boundaries*, *Permissions and approvals*, *Tests and evidence*) are checked by the PR security gate ([SECURITY_REVIEW.md](./SECURITY_REVIEW.md)). |
| **One source of truth** | Each topic has one owning document (see "Documentation ownership" in [README.md](./README.md)). Link to it instead of copying its content. |
| **Honest status** | Do not mark anything as implemented or tested unless it actually runs and was verified. |
