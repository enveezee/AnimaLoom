#!/bin/bash

# Ensure a commit message is provided
if [ -z "$1" ]; then
  echo "Usage: $0 \"<commit message>\""
  exit 1
fi

COMMIT_MESSAGE="$1"
PROJECT_ROOT=$(dirname "$(dirname "$0")") # This script is in AnimaLoom/tools/, so PROJECT_ROOT is AnimaLoom/
BACKUP_DIR="$PROJECT_ROOT/backups"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_FILE="$BACKUP_DIR/AnimaLoom_backup_$TIMESTAMP.tar.gz"

echo "--- AnimaLoom Save Script ---"

# 1. Generate Test Report
echo "Generating test report..."
"$PROJECT_ROOT/tools/run_all_tests.py"

# 2. Git Operations
echo "Adding all changes to Git..."
git add .

echo "Committing changes with message: \"$COMMIT_MESSAGE\""
git commit -m "$COMMIT_MESSAGE"

if [ $? -eq 0 ]; then
  echo "Git commit successful."
else
  echo "Git commit failed or no changes to commit."
fi

# 2. Create Source Backup
echo "Creating source backup..."
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_FILE" -C "$PROJECT_ROOT" --exclude="backups" .

if [ $? -eq 0 ]; then
  echo "Source backup created: $BACKUP_FILE"
else
  echo "Source backup failed."
fi

echo "--- Save Complete ---"
