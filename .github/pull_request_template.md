# Heimdall — Pull Request template

> Every PR must explain its security impact, even if it only changes documents.
> This statement is reviewed by the PR security gate and a human reviewer.
> Empty headings or unfilled placeholders fail the automated gate.

## Summary

<!-- Describe the change and link related requirement / UC / issue. -->

## Security impact

<!-- Which attack surface changes? Say "Documentation only — no runtime behavior or permissions changed" if applicable, with a reason. -->

## Untrusted inputs and trust boundaries

<!-- List untrusted inputs (user, web, OCR/PDF, RAG, memory, model/tool results) and where they are validated, segregated or rejected. If none, explain why. -->

## Permissions and approvals

<!-- List tool/credential scopes, possible side effects, human approvals, payment/external actions, and enforcement outside the LLM. If unchanged, say so explicitly. -->

## Tests and evidence

<!-- What was run and with what result? Include normal, negative, malicious-input and recovery tests where appropriate. Do not claim unexecuted tests passed. -->

## Build vs Reuse

<!-- Which existing Heimdall module / library is reused? What was built and why? Mention licensing, supply chain and service permissions when relevant. -->

## Security review checklist

- [ ] No external text, memory, tool or OCR output is promoted into trusted instructions.
- [ ] LLM-generated plans/tool arguments are validated against deterministic policy before execution.
- [ ] Sensitive actions require appropriate authenticated approval; no implicit spending or checkout.
- [ ] Agents and tools have the minimum necessary permissions; secrets and personal data are minimized.
- [ ] Failures, retries, duplicate events and cancellation cannot cause repeated side effects.
- [ ] Untrusted input cannot be used for command execution, arbitrary URLs/SSRF, unsafe SQL/HTML or unrestricted file access.
- [ ] Relevant abuse/prompt-injection tests are documented and executed, or a test gap is recorded.
- [ ] Any modified security gate, workflow, authorization rule, or approval policy receives independent review.

Security references: [SECURITY_REVIEW.md](../SECURITY_REVIEW.md), [PRINCIPLES.md](../PRINCIPLES.md).
