#!/bin/bash
# Setup script for Docker deployment of the API service using uv

set -e

echo "🐳 ==== Provet API Docker Setup (with uv) ==== 🐳"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "🔗 Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "🔗 Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create directories if they don't exist
mkdir -p solution temp_uploads

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env-template .env
    echo "🔑 Please edit .env file to add your OpenAI API key."
    echo "⚠️ API service will not start without a valid API key."
    echo "⏳ Press any key to continue after editing the .env file..."
    read -n 1 -s
fi

# Build Docker image
echo "🏗️ Building Docker image (using uv for dependency management)..."
docker build -t provet-api .

# Start the service with Docker Compose
echo "🚀 Starting API service with Docker Compose..."
docker-compose up -d

echo "✅ ==== Docker Setup Complete ==== ✅"
echo "🌐 The API service is now running at http://localhost:8000"
echo "📚 API documentation is available at http://localhost:8000/docs"
echo ""
echo "🛠️ Useful commands:"
echo "- 📊 Check container status: docker-compose ps"
echo "- 📋 View logs: docker-compose logs -f"
echo "- ⏹️ Stop the service: docker-compose down"
echo "- 🔄 Rebuild and restart: ./scripts/setup_docker.sh" 