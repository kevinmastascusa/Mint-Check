#!/bin/bash
# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "Working directory is not clean. Please commit or stash changes before proceeding."
    exit 1
fi
# Proceed with rewriting history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch data/GitHubDesktopSetup-x64.exe" \
  --prune-empty --tag-name-filter cat -- --all
