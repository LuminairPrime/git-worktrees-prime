"""Disposable Git checks for documented recovery/preservation, not model behavior."""
from pathlib import Path
import subprocess
import tempfile
import unittest


class GitBehavior(unittest.TestCase):
    def test_repair_preserves_branch_index_and_draft(self):
        with tempfile.TemporaryDirectory(prefix="worktree-repair-") as directory:
            root = Path(directory)
            primary, old, current = [root / name for name in ("primary", "task old", "task current")]
            def git(path, *args):
                return subprocess.run(["git", "-C", str(path), *args], check=True,
                                      capture_output=True).stdout
            primary.mkdir()
            git(primary, "init", "-b", "main")
            git(primary, "config", "user.name", "Fixture")
            git(primary, "config", "user.email", "fixture@example.invalid")
            (primary / "tracked.txt").write_text("original\n")
            git(primary, "add", "tracked.txt")
            git(primary, "commit", "-m", "Initial")
            git(primary, "worktree", "add", "-b", "task/adapter", str(old))
            (old / "tracked.txt").write_text("staged\n")
            git(old, "add", "tracked.txt")
            (old / "draft.txt").write_text("valuable draft\n")
            before_head = git(old, "rev-parse", "HEAD")
            before_index = git(old, "diff", "--cached")
            # Intentional external relocation confined to this disposable fixture.
            old.rename(current)
            git(primary, "worktree", "repair", str(current))
            inventory = git(primary, "worktree", "list", "--porcelain", "-z").split(b"\0")
            self.assertIn(b"worktree " + str(current).encode(), inventory)
            self.assertNotIn(b"worktree " + str(old).encode(), inventory)
            self.assertEqual(git(current, "branch", "--show-current").strip(), b"task/adapter")
            self.assertEqual(git(current, "rev-parse", "HEAD"), before_head)
            self.assertEqual(git(current, "diff", "--cached"), before_index)
            self.assertEqual((current / "draft.txt").read_text(), "valuable draft\n")

    def test_clean_status_does_not_protect_ignored_data(self):
        with tempfile.TemporaryDirectory(prefix="worktree-preserve-") as directory:
            root = Path(directory)
            primary, task = root / "primary", root / "task"
            def git(path, *args):
                return subprocess.run(["git", "-C", str(path), *args], check=True,
                                      capture_output=True).stdout
            primary.mkdir()
            git(primary, "init", "-b", "main")
            git(primary, "config", "user.name", "Fixture")
            git(primary, "config", "user.email", "fixture@example.invalid")
            (primary / ".gitignore").write_text("review.db\n")
            git(primary, "add", ".gitignore")
            git(primary, "commit", "-m", "Ignore review database")
            git(primary, "worktree", "add", "-b", "task/review", str(task))
            valuable = b"non-reproducible review data"
            (task / "review.db").write_bytes(valuable)
            self.assertEqual(git(task, "status", "--short"), b"")
            self.assertIn(b"review.db", git(task, "status", "--short", "--ignored"))
            preserved = root / "preserved.db"
            preserved.write_bytes((task / "review.db").read_bytes())
            git(primary, "worktree", "remove", str(task))
            self.assertFalse(task.exists())
            self.assertEqual(preserved.read_bytes(), valuable)
            git(primary, "show-ref", "--verify", "refs/heads/task/review")


if __name__ == "__main__":
    unittest.main()
