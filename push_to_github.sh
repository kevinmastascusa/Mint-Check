#!/bin/bash
git init
# Add the large file to .gitignore
echo "data/GitHubDesktopSetup-x64.exe" >> .gitignore
git add .gitignore
git add .
# Remove the large file from the index if it was added
git rm --cached data/GitHubDesktopSetup-x64.exe
git commit -m "Initial commit excluding large file"
git remote add origin https://github.com/kevinmastascusa/Mint-Check.git
git push -u origin master

