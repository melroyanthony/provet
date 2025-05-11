#!/bin/bash
# Setup script for CLI usage with uv

set -e

echo "💻 ==== Provet CLI Setup ==== 💻"

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
        echo "❌ uv is required for setup. Exiting."
        exit 1
    fi
fi

# Create virtual environment specifically for CLI
ENV_DIR=".venv-cli"
if [ ! -d "$ENV_DIR" ]; then
    echo "🔧 Creating CLI virtual environment..."
    uv venv "$ENV_DIR" --python 3.13.3
fi

# Activate virtual environment
echo "🚀 Activating CLI virtual environment..."
source "$ENV_DIR/bin/activate"

# Install dependencies using uv sync for main deps only
echo "📦 Installing CLI dependencies with uv..."
uv sync --no-group dev --no-group test --no-group api
uv lock --upgrade

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env-template .env
    echo "🔑 Please edit .env file to add your OpenAI API key."
fi

# Create directories if they don't exist
mkdir -p solution temp_uploads

# Make CLI script executable
chmod +x provet_cli.py

echo "✅ ==== CLI Setup Complete ==== ✅"
echo "🟢 CLI virtual environment is now activated"
echo ""
echo "📚 To use the CLI:"
echo "1️⃣ Activate the virtual environment: source $ENV_DIR/bin/activate"
echo "2️⃣ Run the CLI: ./provet_cli.py [input_file.json]"
echo "   or: python -m provet [input_file.json]"
echo ""
echo "⏹️ To deactivate the virtual environment: deactivate" 