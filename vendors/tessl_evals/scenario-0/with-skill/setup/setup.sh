#!/bin/bash
set -e

# Initialize a local git repository for the myproject backend service
mkdir -p myproject
cd myproject

git init
git config user.email "dev@example.com"
git config user.name "Developer"

# First commit on main (production-only branch)
cat > README.md << 'READMEEOF'
# MyProject

A backend service for managing application configurations.

## Branching Workflow

- **`main`** — production-ready releases only. Do not develop directly on this branch.
- **`develop`** — integration branch for all feature work. Open pull requests against `develop`.

All new features should branch from `develop`.
READMEEOF

git add README.md
git commit -m "Initial project setup"

# Create develop as the integration branch with feature work
git checkout -b develop

mkdir -p src tests

touch src/__init__.py

cat > src/config.py << 'PYEOF'
"""Configuration loader for the backend service."""


def load_config(path: str) -> dict:
    """Load a JSON config from the given file path."""
    import json
    with open(path) as f:
        return json.load(f)
PYEOF

git add .
git commit -m "Add config loader module"

touch tests/__init__.py

cat > tests/test_config.py << 'PYEOF'
import json
import tempfile
import os
from src.config import load_config


def test_load_simple_config():
    data = {"host": "localhost", "port": 5432}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        path = f.name
    try:
        result = load_config(path)
        assert result == data
    finally:
        os.unlink(path)
PYEOF

git add .
git commit -m "Add config loader tests"

# Leave the repo on main so the integration target is not immediately obvious
git checkout main

echo ""
echo "Repository initialized successfully."
echo "Location: $(pwd)"
echo ""
git log --oneline --graph --all
echo ""
echo "Current branch: $(git branch --show-current)"
