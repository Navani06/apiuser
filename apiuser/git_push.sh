#!/bin/bash

echo ""
echo "========================================"
echo "   Git Setup Script — User API"
echo "========================================"
echo ""

echo "✅ Step 1: Initializing Git repository..."
git init

echo ""
echo "✅ Step 2: Setting default branch to main..."
git branch -M main

echo ""
echo "✅ Step 3: Staging all files..."
git add .

echo ""
echo "✅ Step 4: Creating first commit..."
git commit -m "Initial commit: User API with FastAPI and SQLite"

echo ""
echo "========================================"
echo "  Now link your GitHub repository"
echo "========================================"
echo ""
echo "👉 Go to https://github.com/new"
echo "   - Repository name: user-api"
echo "   - Visibility: Public"
echo "   - Do NOT tick README or .gitignore"
echo "   - Click Create repository"
echo ""
read -p "🔗 Paste your GitHub repo URL here: " REPO_URL

if [ -z "$REPO_URL" ]; then
  echo "❌ No URL entered. Exiting."
  exit 1
fi

echo ""
echo "✅ Step 5: Adding remote origin..."
git remote add origin "$REPO_URL"

echo ""
echo "✅ Step 6: Pushing to GitHub..."
git push -u origin main

echo ""
echo "========================================"
echo "🎉 Done! Your code is now on GitHub."
echo "   Visit: $REPO_URL"
echo "========================================"
