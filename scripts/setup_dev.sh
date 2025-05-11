#!/bin/bash
# Setup script for local development using uv

set -e

echo "🛠️ ==== Provet Development Environment Setup ==== 🛠️"

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "🔍 uv not found. Would you like to install it? (y/n)"
    read -r install_uv
    if [[ "$install_uv" =~ ^[Yy]$ ]]; then
        echo "📥 Installing uv..."
        curl -fsSL https://astral.sh/uv/install.sh | bash
        # Make sure uv is in the PATH
        export PATH="$HOME/.cargo/bin:$PATH"
    else
        echo "❌ uv is required for development. Exiting."
        exit 1
    fi
fi

# Create virtual environment
ENV_DIR=".venv"
if [ ! -d "$ENV_DIR" ]; then
    echo "🔧 Creating virtual environment..."
    uv venv "$ENV_DIR" --python 3.13.3
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env-template .env
    echo "🔑 Please edit .env file to add your OpenAI API key."
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source "$ENV_DIR/bin/activate"

# Install dependencies with uv
echo "📦 Installing dependencies with uv..."
uv sync --all-groups
uv lock --upgrade

# Create directories if they don't exist
mkdir -p solution temp_uploads

echo "✅ ==== Development Environment Setup Complete ==== ✅"
echo "🟢 Virtual environment: $ENV_DIR is now activated"
echo "🧪 To run tests: python -m pytest"
echo "💻 To run the CLI: python -m provet"
echo ""
echo "📌 To activate this environment in the future, run:"
echo "source $ENV_DIR/bin/activate" 