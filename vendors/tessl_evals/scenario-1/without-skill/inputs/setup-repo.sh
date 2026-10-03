#!/usr/bin/env bash
set -e

echo "Setting up project repository..."

mkdir -p project-repo
cd project-repo

git init -b develop
git config user.email "dev@example.com"
git config user.name "Dev Team"

# Initial commit on develop
cat > README.md << 'MDEOF'
# Data Pipeline

A data ingestion and processing pipeline for structured log records.
MDEOF
git add README.md
git commit -m "Initial project setup"

# Create feature branch with parser improvements
git checkout -b feature/improve-parser

cat > parser.py << 'PYEOF'
def parse_record(line):
    """Parse a single data record from a log line."""
    parts = line.strip().split(",")
    if len(parts) < 3:
        return None
    return {
        "id": parts[0],
        "timestamp": parts[1],
        "value": float(parts[2])
    }

def parse_batch(lines):
    """Parse a batch of records, skipping malformed ones."""
    results = []
    for line in lines:
        record = parse_record(line)
        if record is not None:
            results.append(record)
    return results
PYEOF
git add parser.py
git commit -m "Add parser module with batch processing support"

# Switch back to develop and squash-merge the feature
git checkout develop
git merge --squash feature/improve-parser
git commit -m "Add parser module with batch processing support (#42)"

# Create the worktree
git worktree add .worktrees/improve-parser feature/improve-parser

echo ""
echo "Setup complete. Repository is at: project-repo/"
echo ""
echo "Current worktree list:"
git worktree list
