#!/bin/bash
# Verify script for Provet Cloud setup

set -e

echo "🔍 ==== Provet Setup Verification ==== 🔍"

# Check project structure
echo "📂 Checking project structure..."
required_dirs=("api" "provet" "data" "solution" "scripts")
missing_dirs=()

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        missing_dirs+=("$dir")
    fi
done

if [ ${#missing_dirs[@]} -gt 0 ]; then
    echo "❌ ERROR: Missing required directories: ${missing_dirs[*]}"
    exit 1
fi

echo "✅ Project structure: OK"

# Check file permissions
echo "🔒 Checking script permissions..."
if [ ! -x "setup.sh" ]; then
    echo "❌ ERROR: setup.sh is not executable"
    exit 1
fi

# This works on macOS and Linux
script_count=$(find scripts -name "*.sh" -type f -perm +111 | wc -l | tr -d ' ')
if [ "$script_count" -lt 4 ]; then
    echo "❌ ERROR: Not all scripts are executable (found $script_count executable scripts)"
    exit 1
fi

echo "✅ Script permissions: OK"

# Check .env file
echo "🌐 Checking environment..."
if [ ! -f ".env" ]; then
    echo "⚠️ WARNING: .env file is missing - the application will not work without API keys"
    echo "🔧 Run one of the setup scripts to create it"
else
    echo "✅ Environment file: OK"
fi

# Determine which setup is active
echo "🔌 Checking active setup..."
if [ -d ".venv" ]; then
    echo "💻 CLI setup (Python venv) is installed"
fi

if [ -f ".python-version" ]; then
    echo "🛠️ Development environment (pyenv) is configured"
fi

if command -v docker-compose &> /dev/null && docker-compose ps | grep -q "provet-api"; then
    echo "🐳 Docker API service is running"
fi

echo "🎉 ==== Verification Complete ==== 🎉"
echo "✨ All checks passed. Provet is ready to use."
echo "🚀 To set up a new environment, run: ./setup.sh" 