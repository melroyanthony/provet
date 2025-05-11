#!/bin/bash
# Cleanup script for Provet Cloud

set -e

echo "🧹 ==== Provet Cleanup ==== 🧹"
echo "⚠️ WARNING: This will remove all local dev environments, virtual envs, and stop Docker containers."
echo "📝 Solution files and data will not be affected."
read -p "🔍 Do you want to continue? (y/n): " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "🛑 Cleanup canceled."
    exit 0
fi

# Stop Docker containers if running
if command -v docker-compose &> /dev/null; then
    echo "🐳 Stopping Docker containers..."
    docker-compose down || true
fi

# Remove Python virtual environments
if [ -d ".venv" ]; then
    echo "🗑️ Removing Python virtual environment (.venv)..."
    rm -rf .venv
fi

if [ -d ".venv-cli" ]; then
    echo "🗑️ Removing CLI virtual environment (.venv-cli)..."
    rm -rf .venv-cli
fi

# Remove uv cache
if [ -d ".uv" ]; then
    echo "🗑️ Removing uv cache..."
    rm -rf .uv
fi

# Remove pytest cache
if [ -d ".pytest_cache" ]; then
    echo "🗑️ Removing pytest cache..."
    rm -rf .pytest_cache
fi

# Remove __pycache__ directories
echo "🗑️ Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "✨ ==== Cleanup Complete ==== ✨"
echo "✅ All local environments have been removed."
echo "🚀 To set up a new environment, run ./setup.sh" 