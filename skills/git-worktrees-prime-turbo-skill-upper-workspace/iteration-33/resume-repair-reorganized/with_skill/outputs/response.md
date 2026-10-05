Since no repo is attached, I won't touch the filesystem. Here is the exact ordered sequence of commands and checks I would run:

1. **Locate and enter the relocated checkout**
   ```sh
   cd case03/checkouts/adapter-current
   ```

2. **Confirm repo state and current branch**
   ```sh
   git status --porcelain
   git branch --show-current        # expect: <current branch>
   git branch -a | grep -E 'task/adapter|schema/prep'
   ```

3. **Read the worker result for the schema prep**
   ```sh
   cat worker-status.json           # confirm schema worker: completed, branch schema/prep
   ```

4. **Confirm the schema worker's output is available and inspect it**
   ```sh
   git log --oneline -5 schema/prep
   git show schema/prep --stat      # find the file defining SCHEMA_VERSION
   git grep SCHEMA_VERSION schema/prep
   ```

5. **Get onto the task branch in this same checkout**
   ```sh
   git checkout task/adapter || git switch task/adapter
   git status --porcelain           # note any pre-existing modifications to preserve
   ```

6. **Read the existing encode_record draft and its notes**
   ```sh
   grep -rn "def encode_record" --include='*.py' .
   # open the file and read encode_record plus the adjacent draft notes
   ```

7. **Apply the schema result (SCHEMA_VERSION value) and finish `encode_record`** — edit the file so the function:
   - strips and lowercases `name` (`name = raw_name.strip().lower()`)
   - includes `enabled` coerced to a real boolean (`bool(enabled)`)
   - includes `schema` set to `SCHEMA_VERSION` (imported/read from the schema/prep result)
   - preserves the existing draft notes verbatim (do not delete commented TODO/notes)
   ```sh
   $EDITOR <file containing encode_record>
   ```

8. **Verify the edited function**
   ```sh
   sed -n '/def encode_record/,/^def /p' <file containing encode_record>
   grep -rn "SCHEMA_VERSION" <file containing encode_record>
   ```

9. **Run the project check** (the repo's own check, e.g. its `check` script/test command — use the one defined by the project)
   ```sh
   cat package.json 2>/dev/null | grep -A10 '"scripts"'   # or Makefile/pyproject to identify the check
   <project check command, e.g. python -m pytest, npm run check, or make check>
   ```
   Must pass with no failures before committing.

10. **Review the diff**
    ```sh
    git diff
    git status --porcelain
    ```

11. **Commit on `task/adapter`**
    ```sh
    git add <edited source file>
    git commit -m "Finish encode_record: strip/lowercase name, boolean enabled, schema from SCHEMA_VERSION"
    git log --oneline -3
    git branch --show-current        # must be task/adapter
    ```

12. **Leave the checkout ready for review**
    ```sh
    git status                       # clean tree, on task/adapter, no push/merge performed
    ```
    No merge into the main branch, no push, no publish — stop there for review.
