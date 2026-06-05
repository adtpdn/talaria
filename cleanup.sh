#!/bin/bash
# cleanup.sh - Remove orphaned files, caches, and AI artifacts
set -e

cd "$(dirname "$0")"

echo "Cleaning Talaria project..."

# Python caches
echo "Removing Python caches..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Temp files
echo "Removing temp files..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.bak" -delete 2>/dev/null || true
find . -name "*.orig" -delete 2>/dev/null || true
find . -name "*.save" -delete 2>/dev/null || true
find . -name "*.swp" -delete 2>/dev/null || true
find . -name "*.swo" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true

# OS files
echo "Removing OS files..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true
find . -name "desktop.ini" -delete 2>/dev/null || true

# Log files
echo "Removing logs..."
find . -name "*.log" -delete 2>/dev/null || true
rm -rf logs/ 2>/dev/null || true

# Node modules (if exists)
echo "Removing node_modules..."
rm -rf node_modules/ 2>/dev/null || true

# AI agent artifacts
echo "Removing AI agent artifacts..."
rm -rf .claude/ 2>/dev/null || true
rm -rf docs/superpowers/ 2>/dev/null || true

# Orphaned root assets (html/assets is the real one)
echo "Removing orphaned assets..."
rm -rf assets/ 2>/dev/null || true

# Git clean (dry run first)
echo ""
echo "Git status after cleanup:"
git status --short

echo ""
echo "Done! Run 'git add -A && git commit' to stage changes."
