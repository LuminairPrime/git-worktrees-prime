#!/usr/bin/env bash
set -euo pipefail

mkdir -p repo/lib repo/config
cd repo

git init -q
git config user.email "dev@example.com"
git config user.name "Developer"

# Initial committed state
cat > lib/parser.py << 'PYEOF'
"""Core parser for dataflow events."""


def parse_event(raw):
    if not isinstance(raw, dict):
        raise ValueError("Event must be a dict")
    return {
        "type": raw.get("type", "unknown"),
        "payload": raw.get("payload", {}),
    }
PYEOF

cat > config/defaults.yaml << 'YAMLEOF'
retry_limit: 3
timeout_ms: 5000
log_level: info
YAMLEOF

cat > README.md << 'READMEEOF'
# dataflow

Internal library for processing analytics events from the data pipeline.
READMEEOF

git add .
git commit -q -m "Initial implementation: event parser and configuration defaults"

# Simulate in-progress modifications left uncommitted (mid-stream work)
cat > lib/parser.py << 'PYEOF'
"""Core parser for dataflow events."""

# WIP: field normalisation refactor -- do not merge yet
_FIELD_MAP = {
    "type": "event_type",
    "payload": "data",
}


def parse_event(raw):
    if not isinstance(raw, dict):
        raise ValueError("Event must be a dict")
    return {_FIELD_MAP.get(k, k): v for k, v in raw.items()}


def normalise_fields(event):
    """Rename legacy fields to canonical names."""
    return {_FIELD_MAP.get(k, k): v for k, v in event.items()}
PYEOF

cat > config/defaults.yaml << 'YAMLEOF'
retry_limit: 5
timeout_ms: 3000
log_level: debug
batch_size: 100
normalise_fields: true
YAMLEOF

echo "Repository initialized at ./repo/ with one committed baseline and two files with uncommitted modifications."
