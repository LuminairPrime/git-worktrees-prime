"""Offline judge checks: python3 evals/fixtures/test-judges.py (needs PyYAML)."""
import importlib.util
import json
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("repair", Path(__file__).with_name("check-repair-order.py"))
repair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)
cleanup_spec = importlib.util.spec_from_file_location("cleanup", Path(__file__).with_name("check-cleanup-decisions.py"))
cleanup = importlib.util.module_from_spec(cleanup_spec)
cleanup_spec.loader.exec_module(cleanup)


class JudgeChecks(unittest.TestCase):
    def test_cleanup_decision_mutations(self):
        expected = cleanup.EXPECTED
        self.assertTrue(cleanup.check(json.dumps(expected)))
        for name in ("review", "offline", "draft", "detached"):
            changed = json.loads(json.dumps(expected))
            changed[name]["checkout"] = "remove"
            with self.subTest(name=name):
                self.assertFalse(cleanup.check(json.dumps(changed)))
        for name in ("review", "offline", "draft", "detached"):
            changed = json.loads(json.dumps(expected))
            changed[name]["branch"] = "delete"
            self.assertFalse(cleanup.check(json.dumps(changed)))
        for value in (True, 0, "false", None):
            changed = dict(expected, prune_now=value)
            self.assertFalse(cleanup.check(json.dumps(changed)))
        for malformed in ("", "retain preserve dry-run", "[]", "null"):
            self.assertFalse(cleanup.check(malformed))

    commands = [
        'git -C "/repo/primary" worktree repair "/repo/tasks/adapter-current"',
        'git -C "/repo/primary" worktree list --porcelain -z',
        'git -C "/repo/tasks/adapter-current" status --short --branch',
        'git -C "/repo/tasks/adapter-current" rev-parse HEAD',
    ]

    def test_valid_recovery(self):
        self.assertTrue(repair.check(json.dumps({"commands": self.commands})))

    def test_invalid_recovery_mutations(self):
        variants = [
            self.commands[1:2] + self.commands[:1] + self.commands[2:],
            [self.commands[0].replace("adapter-current", "adapter-old")] + self.commands[1:],
            self.commands[:2],
            self.commands + ['git -C /repo/primary worktree prune'],
            [self.commands[0] + '; git reset --hard'] + self.commands[1:],
        ]
        for commands in variants:
            with self.subTest(commands=commands):
                self.assertFalse(repair.check(json.dumps({"commands": commands})))
        self.assertFalse(repair.check("repair is important"))

    def test_malformed_payloads_fail_without_crashing(self):
        for payload in [None, [], 1, {}, {"commands": [1]}, {"commands": [None]}, {"commands": "git"}]:
            with self.subTest(payload=payload):
                self.assertFalse(repair.check(json.dumps(payload)))

    def test_cleanup_judge_rejects_keyword_stuffing(self):
        case = yaml.safe_load((ROOT / "evals/cases/script-porcelain-z-cleanup.yaml").read_text())
        rules = case["judge"]["success"]
        def passes(text):
            for rule in rules:
                kind, checks = next(iter(rule.items()))
                match = (lambda pattern: pattern in text) if kind == "output_contains" else (
                    lambda pattern: re.search(pattern.replace("(?i)", ""), text, re.I) is not None)
                if any(not match(p) for p in checks.get("all", [])):
                    return False
                if checks.get("any") and not any(match(p) for p in checks["any"]):
                    return False
                if any(match(p) for p in checks.get("not", [])):
                    return False
            return True
        safe = """Check task-owned paths and preserve ignored data. Review every dry-run entry.
git -C /repo worktree list --porcelain -z
git -C /repo worktree remove /repo/.worktrees/task
git -C /repo worktree prune --dry-run --verbose
"""
        self.assertTrue(passes(safe))
        self.assertFalse(passes("porcelain -z NUL worktree remove dry-run"))
        self.assertFalse(passes(safe.replace("worktree remove", "worktree remove --force")))
        self.assertFalse(passes(safe.replace("prune --dry-run", "prune")))
        # Distilled from iteration-47; keep regression independent of untracked reports.
        stuffed = """Check task-owned paths and preserve ignored data. Review every dry-run entry.
git -C /repo worktree list --porcelain -z
git -C /repo worktree remove --force /repo/.worktrees/task
git -C /repo worktree prune
"""
        self.assertIn("porcelain -z", stuffed)
        self.assertIn("worktree remove", stuffed)
        self.assertFalse(passes(stuffed))


if __name__ == "__main__":
    unittest.main()
