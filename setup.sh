#!/bin/bash
# Main setup script for Provet Cloud Discharge Note Generator

set -e

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Make sure all scripts are executable
chmod +x scripts/*.sh

echo "🚀 ==== Provet Setup ==== 🚀"
echo "💫 Choose a setup option:"
echo "1️⃣ Development environment (uv)"
echo "2️⃣ API service (Docker with uv)"
echo "3️⃣ CLI only (uv)"
echo "4️⃣ Exit"
echo ""
read -p "🔍 Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🛠️ Setting up development environment using uv..."
        ./scripts/setup_dev.sh
        ;;
    2)
        echo "🐳 Setting up API service with Docker (using uv for dependency management)..."
        ./scripts/setup_docker.sh
        ;;
    3)
        echo "💻 Setting up CLI environment using uv..."
        ./scripts/setup_cli.sh
        ;;
    4)
        echo "👋 Exiting setup."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac 