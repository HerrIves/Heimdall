"""Tests for the deterministic security pre-screen (not runtime LLM attack tests)."""

import tempfile
import unittest
from pathlib import Path

from scripts.security_gate import changed_files, iter_added_lines, missing_pr_sections, run, scan_diff


HEADER = """## Security impact
Documentation only; no executable permissions changed.

## Untrusted inputs and trust boundaries
No new untrusted input paths.

## Permissions and approvals
No change to capabilities or approvals.

## Tests and evidence
Reviewed markdown links and linted the PR description.
"""


class DiffParsingTests(unittest.TestCase):
    def test_tracks_line_numbers_for_added_lines(self):
        diff = "\n".join([
            "diff --git a/app.py b/app.py",
            "--- a/app.py",
            "+++ b/app.py",
            "@@ -10,0 +11,2 @@",
            "+safe = True",
            "+eval(untrusted)",
        ])
        self.assertEqual(list(iter_added_lines(diff)), [
            ("app.py", 11, "safe = True"),
            ("app.py", 12, "eval(untrusted)"),
        ])
        self.assertEqual(changed_files(diff), {"app.py"})

    def test_non_code_docs_do_not_trigger_heuristic(self):
        diff = "\n".join([
            "+++ b/SECURITY.md",
            "@@ -0,0 +1,2 @@",
            "+Do not call eval(user_input)",
            "+Never use permissions: write-all",
        ])
        self.assertEqual(scan_diff(diff), [])

    def test_flags_shell_and_dynamic_eval(self):
        diff = "\n".join([
            "+++ b/agent/service.py",
            "@@ -1,0 +1,2 @@",
            "+result = eval(model_text)",
            "+subprocess.run(cmd, shell=True)",
        ])
        findings = scan_diff(diff)
        self.assertEqual([f.rule_id for f in findings], ["HMD-001", "HMD-002"])
        self.assertTrue(all(f.severity == "error" for f in findings))

    def test_flags_privileged_workflow(self):
        diff = "\n".join([
            "+++ b/.github/workflows/unsafe.yml",
            "@@ -0,0 +1,2 @@",
            "+  pull_request_target:",
            "+permissions: write-all",
        ])
        self.assertEqual({f.rule_id for f in scan_diff(diff)}, {"HMD-004", "HMD-005"})

    def test_flags_trust_bypass_as_warning(self):
        diff = "\n".join([
            "+++ b/agent/action.py",
            "@@ -0,0 +1 @@",
            "+auto_approve = True",
        ])
        findings = scan_diff(diff)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "warning")


class PrDescriptionTests(unittest.TestCase):
    def test_complete_pr_body(self):
        self.assertEqual(missing_pr_sections(HEADER), [])

    def test_missing_pr_section(self):
        self.assertEqual(missing_pr_sections("## Security impact\nN/A"), list((
            "Security impact", "Untrusted inputs and trust boundaries",
            "Permissions and approvals", "Tests and evidence",
        )))

    def test_unfilled_html_comment_is_not_evidence(self):
        self.assertIn("Security impact", missing_pr_sections(
            "<!-- Please review changes -->\n## Security impact\n<!-- Write here -->\n"
        ))

    def test_passes_doc_only_with_complete_review(self):
        diff = "+++ b/README.md\n@@ -0,0 +1 @@\n+hello"
        self.assertEqual(run(diff, HEADER), 0)

    def test_blocks_dangerous_change(self):
        diff = "+++ b/app.py\n@@ -0,0 +1 @@\n+exec(model_output)"
        self.assertEqual(run(diff, HEADER), 1)


if __name__ == "__main__":
    unittest.main()
