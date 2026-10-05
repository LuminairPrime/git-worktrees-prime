#!/usr/bin/env python3
"""Grade concrete cleanup choices; never execute model-supplied commands."""
import json
import os
import sys

EXPECTED = {
    "review": {"checkout": "retain", "branch": "retain"},
    "offline": {"checkout": "retain", "branch": "retain"},
    "complete": {"checkout": "remove", "branch": "delete"},
    "draft": {"checkout": "preserve_then_remove", "branch": "retain"},
    "detached": {"checkout": "preserve_then_remove", "branch": "retain"},
    "prune_now": False,
}


def check(message):
    text = message.strip()
    if text.startswith("```") and text.endswith("```"):
        text = "\n".join(text.splitlines()[1:-1])
    try:
        result = json.loads(text)
    except (ValueError, TypeError):
        return False
    # Strict boolean: JSON 0 must not compare equal to False and pass.
    return (isinstance(result, dict) and result.get("prune_now") is False
            and result == EXPECTED)


if __name__ == "__main__":
    passed = check(os.environ.get("EVAL_FINAL_MESSAGE", ""))
    print("Cleanup choices accepted" if passed else
          "Incorrect checkout, branch, preservation or prune decision")
    sys.exit(0 if passed else 1)
