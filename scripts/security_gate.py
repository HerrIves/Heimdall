#!/usr/bin/env python3
"""Heimdall PR security gate (dependency-free, conservative static pre-screen).

This catches a limited set of dangerous code patterns and verifies that each PR
describes its security impact. It does NOT prove the absence of prompt injection
or other vulnerabilities. A separate independent human security review is needed.

Output uses GitHub workflow commands for file/line annotations, and GITHUB_STEP_SUMMARY.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import subprocess
import sys


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    path: str
    line: int
    description: str
    remediation: str


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    pattern: re.Pattern[str]
    description: str
    remediation: str
    workflows_only: bool = False


CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".sh", ".bash", ".yml", ".yaml"}

RULES = (
    Rule("HMD-001", "error", re.compile(r"\b(?:eval|exec)\s*\("),
         "Dynamic evaluation may execute attacker-controlled text.",
         "Use a fixed parser, typed schema and allowlisted operation instead of eval/exec."),
    Rule("HMD-002", "error", re.compile(r"\bshell\s*=\s*True\b|(?:\bos\.system|\bexecSync|\bchild_process\.exec)\s*\("),
         "Shell execution can turn model/tool output into command injection.",
         "Avoid a shell; pass a fixed executable plus validated argument array and restricted runtime."),
    Rule("HMD-003", "error", re.compile(r"\bverify\s*=\s*False\b|\brejectUnauthorized\s*:\s*false\b|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*['\"]?0\b"),
         "TLS certificate validation appears to be disabled.",
         "Enable certificate verification and configure an explicit trusted certificate bundle if needed."),
    Rule("HMD-004", "error", re.compile(r"\bpermissions\s*:\s*write-all\b"),
         "GitHub Actions receives unnecessarily broad write permissions.",
         "Set explicit least-privilege job permissions (normally contents: read).", True),
    Rule("HMD-005", "error", re.compile(r"\bpull_request_target\s*:"),
         "Privileged pull_request_target is dangerous if it checks out or runs untrusted PR code.",
         "Prefer pull_request with read-only permissions; independently review any exception.", True),
    Rule("HMD-006", "error", re.compile(r"(?:\bcurl\b|\bwget\b)[^\n|]{0,350}\|\s*(?:bash|sh)\b"),
         "Remote shell script is executed without a reviewed, pinned artifact.",
         "Use a vetted, pinned release with signature/checksum verification; do not pipe downloads to a shell."),
    Rule("HMD-007", "warning", re.compile(r"\b(?:innerHTML\s*=|dangerouslySetInnerHTML\b)"),
         "Untrusted content may be rendered as executable HTML.",
         "Use safe text rendering; if HTML is necessary, apply contextual sanitization and CSP."),
    Rule("HMD-008", "warning", re.compile(r"\b(?:auto[_-]?approve|skip[_-]?permission[_-]?check|bypass[_-]?approval|disable[_-]?auth)\b", re.IGNORECASE),
         "A change may weaken agent permissions or user confirmation.",
         "Keep risk-based policy enforcement outside the LLM; add denial and forged-approval regression tests."),
    Rule("HMD-009", "warning", re.compile(r"\b(?:secrets\s*:\s*inherit)\b"),
         "A workflow inherits secrets more broadly than necessary.",
         "Pass only the specifically required secret to a reviewed job and never to untrusted PR execution.", True),
)

REQUIRED_PR_SECTIONS = (
    "Security impact",
    "Untrusted inputs and trust boundaries",
    "Permissions and approvals",
    "Tests and evidence",
)

SENSITIVE_FRAGMENTS = (
    ".github/workflows/", "security_gate.py", "/auth/", "/policy/",
    "/agent/", "/agents/", "/tools/", "/payment/", "/payments/", "/prompts/",
)


def iter_added_lines(diff: str):
    """Yield (file, new-file line number, added content) from a zero-context git diff."""
    path = None
    line_number = None
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
            line_number = None
        elif line.startswith("+++ /dev/null"):
            path = None
            line_number = None
        elif line.startswith("@@ "):
            match = re.search(r"\+(\d+)(?:,\d+)?\s+@@", line)
            line_number = int(match.group(1)) if match else None
        elif path is not None and line_number is not None:
            if line.startswith("+") and not line.startswith("+++"):
                yield path, line_number, line[1:]
                line_number += 1
            elif line.startswith(" "):
                line_number += 1


def changed_files(diff: str) -> set[str]:
    return set(re.findall(r"(?m)^\+\+\+ b/(.+)$", diff))


def scan_diff(diff: str) -> list[Finding]:
    findings = []
    for path, line_number, text in iter_added_lines(diff):
        if Path(path).suffix.lower() not in CODE_SUFFIXES:
            continue
        stripped = text.lstrip()
        if stripped.startswith(("#", "//", "*", "--")):
            continue
        is_workflow = path.startswith(".github/workflows/") and Path(path).suffix.lower() in {".yml", ".yaml"}
        for rule in RULES:
            if rule.workflows_only and not is_workflow:
                continue
            if rule.pattern.search(text):
                findings.append(Finding(rule.rule_id, rule.severity, path, line_number, rule.description, rule.remediation))
    return findings


def missing_pr_sections(body: str | None) -> list[str]:
    cleaned = re.sub(r"<!--.*?-->", "", body or "", flags=re.DOTALL)
    missing = []
    for name in REQUIRED_PR_SECTIONS:
        regex = rf"(?im)^##\s+{re.escape(name)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
        match = re.search(regex, cleaned)
        value = match.group(1).strip() if match else ""
        if not value or value.lower() in {"todo", "tbd", "n/a", "none", "-", "..."}:
            missing.append(name)
    return missing


def _command(value: str) -> str:
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def annotate(finding: Finding) -> None:
    # Git path names can be attacker-controlled: never embed unusual characters
    # into the workflow command's file argument.
    safe_path = re.fullmatch(r"[A-Za-z0-9_./-]+", finding.path) is not None
    prefix = "::error" if finding.severity == "error" else "::warning"
    fields = f" file={finding.path},line={finding.line},title={finding.rule_id}" if safe_path else f" title={finding.rule_id}"
    print(f"{prefix}{fields}::{_command(finding.description + ' Fix: ' + finding.remediation)}")


def get_diff(base: str, head: str) -> str:
    if not all(re.fullmatch(r"[a-fA-F0-9]{40}", sha) for sha in (base, head)):
        raise ValueError("Expected full 40-character commit SHAs.")
    process = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--no-textconv", "--unified=0",
         "--diff-filter=ACMRT", f"{base}...{head}", "--"],
        check=True, text=True, capture_output=True, timeout=90,
    )
    return process.stdout


def run(diff: str, body: str | None) -> int:
    findings = scan_diff(diff)
    changed = changed_files(diff)
    required = missing_pr_sections(body)
    for name in required:
        print("::error title=Security review incomplete::" +
              _command(f"PR description needs a substantive '## {name}' section. "
                       "Explain the trust boundary or why the change has no impact."))

    for finding in findings:
        annotate(finding)

    for path in sorted(changed):
        if any(fragment in f"/{path.lower()}" for fragment in SENSITIVE_FRAGMENTS):
            print("::warning title=Security-sensitive change::" +
                  _command(f"Review {path} for tool privileges, prompt injection, "
                           "exfiltration, approval bypass and security-gate tampering."))

    failures = sum(item.severity == "error" for item in findings) + len(required)
    summary = [
        "## Heimdall — PR security gate",
        f"- Scanned {len(changed)} changed files ({len(findings)} heuristic findings).",
        f"- Blocking patterns: {sum(x.severity == 'error' for x in findings)}.",
        f"- Advisory warnings: {sum(x.severity == 'warning' for x in findings)}.",
        f"- Missing security review sections: {len(required)}.",
        "",
        "**This gate is a limited static pre-screen, NOT a prompt-injection proof or a human approval.**",
        "External documents, web pages, RAG content and model tool calls need runtime policy enforcement, "
        "isolation, authenticated authorization and adversarial tests.",
        "",
    ]
    if findings:
        summary += ["| Severity | Location | Finding | Suggested fix |", "| --- | --- | --- | --- |"]
        for x in findings:
            safe = lambda s: s.replace("|", "\\|").replace("\n", " ")
            summary.append(f"| {x.severity} | {safe(x.path)}:{x.line} | {x.rule_id}: {safe(x.description)} | {safe(x.remediation)} |")
    if required:
        summary += ["", "### Missing PR security sections", *[f"- {name}" for name in required]]
    summary += ["", "### Next review layer",
                "A maintainer must still inspect untrusted-source boundaries, tool permissions, "
                "model-to-action transitions, secret access, data flow and risk-based approvals."]
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as file:
            file.write("\n".join(summary) + "\n")
    else:
        print("\n".join(summary))

    if failures:
        print(f"Security gate FAILED: {failures} blocking problem(s).", file=sys.stderr)
        return 1
    print("Security pre-screen passed. Human review and runtime tests still required.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--event", required=True, help="Path to GitHub PR event JSON")
    args = parser.parse_args()
    try:
        event = json.loads(Path(args.event).read_text(encoding="utf-8"))
        if "pull_request" not in event:
            raise ValueError("Only pull_request events are supported by this gate.")
        return run(get_diff(args.base, args.head), event["pull_request"].get("body"))
    except (ValueError, OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"::error title=Security gate infrastructure failed::{_command(str(exc))}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
