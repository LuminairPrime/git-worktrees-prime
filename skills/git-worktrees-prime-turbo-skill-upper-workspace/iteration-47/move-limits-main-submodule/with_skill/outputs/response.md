Based on the Git worktree skill, here is the answer:

## Do NOT use `git worktree move`

`git worktree move` **cannot move main worktrees or submodule-containing worktrees**. Both of your checkouts fall into unsupported categories. Using it will fail or corrupt the registration.

## Correct procedure: `mv` + `git worktree repair`

The supported approach is to relocate with filesystem tools (preserving `.git` and all contents), then reconnect each checkout with `git worktree repair` run from the main checkout.

---

### Pre-move checks (run from each worktree)

```sh
# 1. Verify clean status — must return empty
git -C /old/main status --porcelain
git -C /old/task  status --porcelain

# 2. Confirm no processes (editors, shells, builds, servers) are running
#    from inside either worktree. Stop them first.

# 3. For the submodule worktree: verify submodule .git files use RELATIVE paths
#    (not absolute). This output should start with "gitdir: …" containing "../"
cat /old/task/<submodule>/.git

# 4. Confirm target directories do not exist or are empty
ls -la /new/main   # should not exist or be empty
ls -la /new/task   # should not exist or be empty
```

If any submodule `.git` file contains an **absolute** path, `mv` will break it. You would need to convert it to a relative path before moving (or re-init the submodule after the move).

---

### Move commands (in order)

```sh
# 1. Move the MAIN worktree first.
#    Its .git is a real directory, so it remains fully functional after the move.
mv /old/main /new/main

# 2. Move the LINKED worktree (with submodules).
#    Its .git file is now broken — that is expected; repair fixes it next.
mv /old/task /new/task

# 3. Repair the linked worktree from the NEW main location.
#    This updates .git/worktrees/<name>/gitdir and the worktree's .git file.
git -C /new/main worktree repair /new/task

# 4. Verify the full inventory — both worktrees should appear with correct paths
git -C /new/main worktree list --porcelain -z

# 5. Verify submodules still resolve in the moved linked worktree
git -C /new/task submodule status
```

---

### Why this order

| Step | Reason |
|------|--------|
| Move **main** first | Its `.git` is a directory, so it works immediately after `mv`. You need a functioning repo to run `repair`. |
| Move **linked** second | Its `.git` file points to `../.git/worktrees/<name>/` relative to the old main location. It is broken after the move — `repair` reconnects it. |
| **Repair** after both moves | `git worktree repair` updates the internal `gitdir` pointers and the worktree's `.git` file to the new absolute paths. |

---

### If a submodule `.git` file was absolute

If step 3 of the pre-move checks revealed an absolute path, either:

- **Fix it before moving:**
  ```sh
  # Run from the submodule's parent worktree
  git -C /old/task submodule absorbgitdirs
  ```
  Then re-check with `cat` to confirm it is now relative.

- **Or re-init after moving:**
  ```sh
  git -C /new/task submodule update --init --recursive
  ```

---

### Summary

| | Main checkout | Linked worktree with submodules |
|---|---|---|
| **`git worktree move`?** | ❌ No — unsupported | ❌ No — unsupported |
| **Correct method** | `mv` + `git worktree repair` | `mv` + `git worktree repair` |
| **Key risk** | None if clean | Submodule `.git` files must use relative paths |
