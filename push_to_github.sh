#!/bin/bash
# Initialize the Git repository if not already initialized
git init
# Stage all changes
git add .
# Commit changes with a message
git commit -m "Initial commit"
# Add the remote repository
git remote add origin https://github.com/kevinmastascusa/Mint-Check.git
# Push changes to GitHub
git push -u origin master
