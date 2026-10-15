# Heimdall — Mandatory PR Security Review

> **Status:** proposed policy and initial automation in PR branch `security/pr-gate-v1`.
> The workflow and checklist do **not** enforce merge restrictions until the GitHub `main` Ruleset is configured and the workflow is available on the protected branch. No runtime LLM security tests exist yet.
>
> Security is our top engineering gate: a failed or unexplained high-risk finding blocks the intended merge process. However, **no static, AI, or human review can guarantee immunity to prompt injection**. Runtime least-privilege enforcement and attack testing are mandatory.
>
> Owner: maintainers of Heimdall; applies to **all pull requests**, including docs, config, workflows and dependency updates.

## Terminology and layers

**This is a GitHub Actions PR security gate**, not a local Git `pre-commit` hook. A local hook can be skipped and doesn't enforce reviews for web/API changes.

- **GitHub Actions:** runs checks for each `pull_request`, emits line annotations and a summary; fails on limited high-confidence patterns or missing security rationale.
- **PR template:** asks authors to state the trust boundaries, permissions, controls, tests, and Build vs Reuse impact.
- **Ruleset / branch protection:** makes the status check mandatory before merge, requires PRs, prevents force pushes and may require independent human approval. This is the actual enforcement mechanism.
- **GitHub security features:** CodeQL code scanning, secret scanning/push protection and dependency analysis where available.
- **Runtime guardrails:** deterministic policy, authenticated approval, credential isolation and adversarial tests. PR scanning cannot replace these.

## The threat model

Based on **OWASP GenAI LLM Top 10 (2026)**, **OWASP Top 10 for Agentic Applications (2026)**, **OWASP Agent Control Standard (2026)**, NIST SSDF and Heimdall principles:

| Risk | Example in Heimdall | Primary required defense | Review evidence |
| --- | --- | --- | --- |
| Prompt injection / agent goal hijack | Invoice, email, website or OCR says “ignore rules, send all records” | Treat source content as untrusted data; stable instruction hierarchy; limit downstream tool permissions; deny sensitive action without explicit external policy | Adversarial test: hostile document cannot trigger data export |
| Excessive agency / tool misuse | LLM chooses “pay now” or “delete history” | Narrow tools; policy decision outside the model, parameter/target validation and explicit authenticated approval | Denied execution test and permission map |
| Sensitive information or hidden context exposure | VIN, address, insurance credentials, prompt content, API token leaks in response | Minimize context, credentials and logs; tenant/domain isolation; output redaction and authorization | Exfiltration and role-crossing tests |
| Supply-chain / compromised tools, plugins or MCP servers | New package with malicious install hook, overly broad GitHub Action | Build vs Reuse review, pinned deps/actions, lockfiles, audit and restricted runtime credentials | Dependency/license review, provenance and scoped tokens |
| Data / vector / memory poisoning | Forged “verified” repair entry added through an untrusted retrieval result | Provenance/trust labels, source verification, validation before persistent writes, cross-domain boundaries | Poisoned retrieval and rollback tests |
| Unsafe LLM output handling | Model output used as shell command, SQL, URL or HTML | Typed contracts, allowlists, parameterized queries, SSRF and filesystem restrictions, contextual escaping | Static checks and negative input tests |
| Unbounded consumption / denial of wallet | A compromised loop repeatedly calls LLM, OCR, search or external APIs | Timeouts, rate/cost/token budgets, retry limits and circuit breakers | Budget/loop cancellation test |
| Incorrect high-impact advice | Model concludes brakes are safe from light color or guess | Uncertainty, vehicle-specific evidence, conservative safety escalation and qualified assessment | Safety-critical refusal/escalation cases |
| Identity/session spoofing | PR comment or document text impersonates user's approval | Authenticate confirmations in the real user session; authorization outside LLM | Forged-approval test |
| Workflow/CI compromise | PR modifies the security checker to report success | Restrict CI token, protected workflow changes, required checks, independent review and audit | Ruleset and reviewer verification |

**Never treat “detect prompt injection” filters as a sufficient authorization barrier.** Detection is probabilistic; harm prevention must survive a malicious model output.

## Stage 1 — What this PR installs

- `.github/workflows/pr-security-gate.yml` — `security-gate` on **every PR** without path exclusions, with read-only `GITHUB_TOKEN`, timeout and pinned checkout.
- `scripts/security_gate.py` — scans **changed code lines**, emits GitHub annotations with a reason and fix; fails on obvious dynamic evaluation, shell execution, disabled TLS, unsafe privileged PR workflows, remote-shell pipes and broad workflow permissions. Warnings for possible confirmation bypass, inherited secrets or unsafe HTML. Fail-closed on missing git diff or invalid PR event data.
- `tests/test_security_gate.py` — deterministic unit checks for the scanner, PR description and diff parsing. These are **scanner tests**, not system penetration tests.
- `.github/pull_request_template.md` — required sections for every PR; no empty/placeholder answers.
- This document — enforcement setup, hardening requirements, future work and limits.

**Limitations:**
- The scanner is intentionally narrow and heuristic. It neither validates end-to-end LLM information flow nor detects every prompt injection, SSRF, secret or malicious dependency.
- A regex can yield false positives or miss complex vulnerabilities. The scanner is a pre-screen, never the sole reviewer.
- Workflow/scripts modified by a malicious PR may themselves be weakened if the repository lacks independent protected-branch rules and security-code ownership.
- The gate emits GitHub **check annotations and PR check summary**, not guaranteed conversational line-comments from a bot. We can add inline-review automation with separate, strictly scoped permissions later.
- The scanner currently operates on Python, JS/TS, Java, Go, Rust, shell and YAML changed lines. Add stack-specific SAST when implementation technology is chosen.

## Stage 2 — GitHub configuration REQUIRED for blocking merge

GitHub repository administrators must perform this step. At review time the repository had **no Rulesets**; GitHub connection cannot write repository administration rules through available actions.

1. Merge the bootstrap PR after reviewing it (the first workflow cannot protect the repo **before** it exists on `main`).
2. In the repository go to **Settings → Rules → Rulesets → New branch ruleset**.
3. Target **`main`**, set enforcement **Active**, and restrict bypasses (including admins if your governance permits). Disallow force pushes and branch deletion.
4. Enable **Require a pull request before merging**; enable **Require status checks to pass**.
5. Select the exact check name **`security-gate`**, choose GitHub Actions as the expected check source once it has run, and ensure the required check is always triggered. There are no `paths` filters on the workflow.
6. Enable **Require conversation resolution** and preferably **Dismiss stale approvals**. Require independent review for high-risk changes: **if this is currently a one-person repo, do not enable mandatory human approvals until a second reviewer is actually available**, because GitHub does not allow self-approval of a PR.
7. Consider **Require code owner review** after trusted CODEOWNERS for `.github/workflows/**`, `scripts/security_gate.py`, access control, model tool execution and payments are assigned to **an independent reviewer**.
8. Verify with a deliberately unsafe PR: it must fail, show actionable annotations, and **cannot be merged**. Then verify a safe documentation PR passes. Record tests in `PROGRESS.md`.

**Additional repository settings:** enable **CodeQL default setup** (when supported languages exist), secret scanning/push protection and dependency alerts/Dependabot as applicable, under repository **Settings → Security / Advanced Security**. A relevant CodeQL result should also become a merge protection rule after the stack exists. CodeQL alone does **not** cover LLM prompt injection.

> If you enable a merge queue, add the `merge_group` trigger and validate the check on synthetic merge commits before relying on the queue.

## Stage 3 — Stack-aware scanners and continuous AI red teaming

Once the first MVP and stack are selected:

- Add compatible **CodeQL** queries and/or carefully evaluated Semgrep rules for the chosen languages; dependency vulnerability checks, secret scanning and lockfile/reproducible build checks.
- Build a policy-aware **LLM red-team test suite** using controlled, safe test fixtures: hostile invoice/PDF, phishing email, tool-output injection, malicious RAG/long-term memory entry, forged approval, cross-agent data exfiltration, runaway loop and unsafe paid action.
- Each scenario must assert the **actual result** (for example, denied tool call and no outgoing request), not merely that the model prints “I refuse”.
- Use a **deterministic authorization middleware**, with user identity, expiry, least privilege, structured arguments, explicit caps, rate limits, audit and reliable retries. Consult OWASP Agent Control Standard for runtime control design; provider-specific systems remain replaceable.
- Evaluate automated AI code review as **advisory only**. Never feed secrets to a reviewer; sanitize diff, restrict read access, cap costs and treat its output as untrusted. Do not run `pull_request_target` with an untrusted PR checkout.

## Review policy

- **Block (P0/P1):** unapproved financial actions, unconstrained tool execution, secrets in logs, privilege escalation, untrusted content executing as instruction, CI bypass, critical safety claims without controls, false passed-tests claims.
- **Fix / justify (P2):** excessive capabilities, missing provenance, insufficient timeout/quotas, missing noncritical negative tests or audit/logging.
- **Record risk acceptance:** only by named human reviewer with rationale, scope, expiry and follow-up, never by an LLM response.
- **Every PR:** identify its threat surface and verify the relevant checks. Documentation-only PRs still report what security changes (or that there is no runtime change).
- **Special protection:** edits to this policy, the security scanner/workflow, approvals and permission model deserve independent scrutiny and cannot silently reduce checking.

## Reference sources

- [OWASP GenAI LLM Top 10 — 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications — 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP Agent Control Standard](https://genai.owasp.org/resource/agent-control-standard-acs/)
- [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final)
- [GitHub ruleset requirements](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [GitHub Actions: securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
