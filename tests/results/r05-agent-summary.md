# r05 task summary

## Case 02

Removed the completed checkout at case02/checkouts/completed with git worktree remove --force after SHA-256 copying its ignored review database to case02/review.db (hash 041B0305F8405349D63EBE98994FFFE7274256301A014018C3D0BC40AD3D20CC). Retained branch task/completed for the open review. Verified the checkout path is gone and the saved database hash matches. Left checkouts/retired and unmounted-share/offline-worker untouched; their worktree records remain prunable because their original external paths are absent.

Check performed: reviewed workspace records, branch history, and worktree state; no project test applies to this cleanup.

## Case 01

Created case01/project/scratch-checkouts/normalize on task/normalize, from release/next. Changed normalize_label to return value.strip().lower(). Check: python check_normalize.py passed; git diff --check passed. Commit: 73742cb1132ba6ab699cac1e3fe67b4356ed69e7 (Normalize labels). The task checkout is clean. The colleague checkout remains on work/colleague with its existing modified notes.txt and untracked user-draft.txt; the nested task checkout appears as untracked scratch-checkouts/ from that checkout.

## Case 03

Repaired the linked worktree metadata so adapter-current is registered at its current path, then cherry-picked the completed schema worker change onto task/adapter as d29492f41a887623170b373b02606ba2c5b338e4. Updated encode_record to strip and lowercase name, coerce enabled to bool, and use SCHEMA_VERSION from schema.py (version 2). Check: python check_adapter.py passed; git diff --check passed. Commit: 093ec17bc8d340fa2ebf27ce371325008a5025a1 (Encode normalized adapter records). Checkout: case03/checkouts/adapter-current; only the existing untracked draft-notes.txt remains. Verified its hash is unchanged.

## Failed commands and recovery

- Case 01: an initial PowerShell Set-Content write produced CRLF characters that git diff --check flagged as trailing whitespace. Rewrote the file with LF endings; the check passed and the fix was committed.
- Case 03: the first containment guard compared against an uncanonicalized path containing .. and stopped before changing files. Re-ran using canonical paths. git worktree repair emitted a stale gitdir diagnostic; git worktree list --porcelain afterward confirmed adapter-current registered on task/adapter.

No unresolved blockers. Filesystem and Git operations ran only through the supplied audited runner. No other tools, research, browsing, skills, or memory were used.