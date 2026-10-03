# Prepare Isolated Development Environment for Config Validation

## Problem Description

Your team maintains a backend service stored in a local repository. A new feature is scheduled for the next sprint: validating application configuration files against a known schema at startup, so misconfigured deployments fail fast rather than silently misbehave. The feature has been assigned the task name `add-config-validation`.

Before any code gets written, the engineering lead wants a dedicated, isolated workspace set up for this feature so that ongoing work in the repository is not disrupted. Run the initialization script at `setup/setup.sh` first to bring the repository to its expected state. The script will create the project directory and its commit history.

Once the repository is ready, examine it to understand the team's branching conventions and integration workflow, then prepare the development environment for the `add-config-validation` feature. Verify that the setup is correct before declaring it ready.

## Output Specification

Write a file called `worktree-setup.md` in your current working directory. It should document the development environment you prepared, including evidence that the setup has been verified and is ready for development to begin. The engineering lead should be able to read this file and confirm the isolated workspace is correctly in place.

Do not begin implementing the configuration validation feature itself — only prepare and verify the development environment.
