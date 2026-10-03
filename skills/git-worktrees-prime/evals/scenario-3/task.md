# Emergency Hotfix Workspace

## Background

You are a developer on the `dataflow` library — a Python analytics event-processing toolkit used by the company's data pipeline. This morning you began reworking two components — the core event parser (`lib/parser.py`) and the configuration defaults (`config/defaults.yaml`) — to add a field-normalisation layer. The work is mid-stream and not yet committed.

Your team has just escalated an urgent production incident: the request handler is crashing with a null-pointer exception under certain API response shapes. The root cause is diagnosed and the fix is small, but it must be delivered as a standalone change. Mixing it with your in-progress normalisation rework would complicate QA's regression isolation and block the release timeline.

A colleague has asked you to create a clean, isolated workspace for the hotfix so it can be built, reviewed, and merged independently — without disturbing your in-progress work.

## Setup

Run the following script to initialise the repository environment:

```bash
bash inputs/setup.sh
```

This creates a local git repository at `./repo/` representing your current development workspace, complete with commit history and the two in-progress file modifications in place.

## Your Task

Work inside `./repo/`. Create an isolated workspace for the `hotfix/null-check` branch so the urgent fix can proceed without interfering with the in-progress rework.

Write a file called `isolation-plan.md` inside `./repo/` that records:

1. What you observed about the current state of the repository before taking any action
2. The decision you made about the in-progress changes and the reasoning behind it
3. The exact steps and commands used to establish the isolated workspace
4. Verification that the isolated workspace is correctly set up and ready for the hotfix

Do not leave any large files on disk when you are done.
