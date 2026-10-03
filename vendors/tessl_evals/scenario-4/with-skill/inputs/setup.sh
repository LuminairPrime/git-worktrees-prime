#!/bin/bash
set -e

mkdir -p repo
cd repo

git init -q
git config user.email "dev@finstream.io"
git config user.name "FinStream Dev"

echo "# Data Processing Service" > README.md
mkdir -p src
echo "def process_batch(items): pass" > src/pipeline.py
git add .
git commit -q -m "Initial commit"

git branch feature/data-pipeline
mkdir -p .worktrees
git worktree add -q .worktrees/data-pipeline feature/data-pipeline

# Add work on the feature branch
cd .worktrees/data-pipeline
echo "def ingest(source, dest): pass" >> src/pipeline.py
git add .
git commit -q -m "WIP: data ingestion stub"
cd ../..

# Simulate the team's mistake: relocate the worktree using mv instead of git worktree move
mv .worktrees/data-pipeline .worktrees/pipeline-v2

echo "Repository initialized at: $(pwd)"
echo "Worktree physically relocated from .worktrees/data-pipeline to .worktrees/pipeline-v2"
