#!/usr/bin/env python3
"""Check the constrained recovery plan; this does not execute Git commands."""
import json
import os
import shlex
import sys


def check(message):
    text = message.strip()
    if text.startswith("```"):
        text = "\n".join(text.splitlines()[1:-1])
    try:
        payload = json.loads(text)
        if not isinstance(payload, dict):
            return False
        commands = payload["commands"]
        if not isinstance(commands, list) or not commands or not all(isinstance(c, str) for c in commands):
            return False
        parsed = [shlex.split(command) for command in commands]
    except (ValueError, KeyError, TypeError):
        return False
    expected = ["git", "-C", "/repo/primary", "worktree", "repair",
                "/repo/tasks/adapter-current"]
    if parsed[0] != expected:
        return False
    # Accept only read-only verification after repair. No shell chaining.
    inventory = status = head = False
    for args in parsed[1:]:
        if args[:3] == ["git", "-C", "/repo/primary"]:
            if args[3:] != ["worktree", "list", "--porcelain", "-z"]:
                return False
            inventory = True
        elif args[:3] == ["git", "-C", "/repo/tasks/adapter-current"]:
            tail = args[3:]
            if tail == ["status", "--short", "--branch"]:
                status = True
            elif tail == ["rev-parse", "HEAD"]:
                head = True
            elif tail != ["rev-parse", "--show-toplevel"]:
                return False
        else:
            return False
    return inventory and status and head


if __name__ == "__main__":
    passed = check(os.environ.get("EVAL_FINAL_MESSAGE", ""))
    print("Recovery plan accepted" if passed else
          "Require repair at the current path first, then inventory, branch/status and HEAD checks")
    sys.exit(0 if passed else 1)
