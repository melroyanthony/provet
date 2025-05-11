# Provet Cloud Discharge Note Generator

![Veterinary Care](https://img.shields.io/badge/Veterinary_Care-LLM_Powered-blue)
![Python](https://img.shields.io/badge/Python-3.13%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Provet is a specialized tool that **automatically generates high-quality discharge notes for veterinary consultations** using OpenAI's language models. The tool processes JSON consultation data to produce comprehensive, professionally formatted discharge notes that veterinarians can provide to pet owners.

## ✨ Features

- 🚀 **Advanced LLM Integration**: Leverages OpenAI's models to generate accurate, contextual discharge notes
- 📋 **Template-Based Generation**: Uses Jinja2 templates for customizable note formatting
- 🔄 **Multiple Deployment Options**: Run as CLI tool, API service, or use in development
- 🐳 **Docker Support**: Containerized deployment for easy scaling
- 📱 **REST API**: Integrate with existing veterinary practice management systems
- ⚙️ **Highly Configurable**: Adjust model parameters and customize system instructions

## 📋 Requirements

- Python 3.13 or higher (or uv which manages Python version for you)
- OpenAI API key

## 🚀 Quick Start

The project supports three different setup methods:

```bash
# Run the interactive setup script
./setup.sh
```

Choose from:
1. **Development environment** (uv) - For contributors and developers
2. **API service** (Docker with uv) - For running the API service
3. **CLI only** (uv) - For simple command-line usage

## 🛠️ Setup Options

### 1. Development Environment (uv)

Best for active development work:

```bash
./scripts/setup_dev.sh
```

**Requirements:**
- uv (installed by the script if needed)

This setup:
- Creates a Python 3.13 virtual environment with uv
- Installs all dependencies using uv (including development tools)
- Sets up environment for local development

### 2. API Service (Docker with uv)

Best for running the API service:

```bash
./scripts/setup_docker.sh
```

**Requirements:**
- Docker
- Docker Compose

This setup:
- Builds the Docker image using uv for dependency management
- Includes a test stage that runs unit tests during the build process
- Starts the API service using Docker Compose
- Exposes the API at http://localhost:8000

### 3. CLI Only (uv)

Best for simple command-line usage:

```bash
./scripts/setup_cli.sh
```

**Requirements:**
- uv (installed by the script if needed)

This setup:
- Creates a separate Python 3.13 virtual environment (.venv-cli) using uv
- Installs only the main required dependencies using uv sync
- Sets up the CLI command for minimal installation

## 💻 Usage

### Command Line

After setting up with any of the options:

```bash
# Using the CLI wrapper script
./provet_cli.py data/consultation1.json

# Or as a Python module
python -m provet data/consultation1.json
```

This will generate a discharge note and save it to a JSON file in the `solution` directory.

You can specify a custom template directory:

```bash
./provet_cli.py data/consultation1.json --template-dir path/to/templates
```

### API Service

When running with the Docker setup:

```bash
# The API is available at
http://localhost:8000

# Swagger UI documentation at
http://localhost:8000/docs
```

## ⚙️ Environment Variables

Copy `.env-template` to `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Additional configuration options:
```
# LLM Configuration
OPENAI_MODEL=gpt-4o
TEMPERATURE=0.7
MAX_TOKENS=800

# Add custom instructions to the system message
CUSTOM_SYSTEM_INSTRUCTION=It is extremely important that you follow the exact format provided in the prompt template. Do not deviate from the section structure or add extra sections.
```

## 📁 Project Structure

```
provet/                 # Core package
├── __init__.py         # Package initialization
├── __main__.py         # Command-line entry point
├── core/               # Core functionality
│   ├── app.py          # Main application (Facade pattern)
│   ├── data_models.py  # Data models using dataclasses
│   ├── io_manager.py   # File I/O operations
│   └── llm_service.py  # Language model interaction
├── templates/          # Jinja2 templates
└── utils/              # Utility modules

api/                    # API service
├── main.py             # FastAPI application
└── __init__.py         # Package initialization

scripts/                # Setup and utility scripts
├── setup_dev.sh        # Development environment setup (uv)
├── setup_docker.sh     # Docker setup for API service (uses uv)
├── setup_cli.sh        # CLI setup with uv
├── cleanup.sh          # Clean up environments
└── verify_setup.sh     # Verify setup requirements

data/                   # Sample input data
├── consultation1.json  # Sample consultation data
└── consultation2.json  # More sample consultation data

solution/               # Generated output files
templates/              # Custom templates (can override defaults)

# Dependency files
pyproject.toml          # Project configuration and dependencies
Dockerfile              # Container definition
docker-compose.yml      # Container orchestration
```

## 🔄 Development Workflow

1. **Initial Setup**: Run `./scripts/setup_dev.sh` to create the development environment
2. **Activate Environment**: Run `source .venv/bin/activate` to activate the development virtual environment
   (Or `source .venv-cli/bin/activate` if you only installed the CLI)
3. **Run Tests**: Run `python -m pytest` to execute tests
4. **Make Changes**: Edit code in the `provet/` directory
5. **Test CLI**: Run `python -m provet data/some_file.json` to test
6. **Test API**: Run `python -m uvicorn api.main:app --reload` for local API testing

## 🐳 Docker Build Process

The Docker build uses a multi-stage process:
1. **Builder stage**: Sets up dependencies and prepares the application code
2. **Test stage**: Runs unit tests to ensure code quality and functionality
3. **Runtime stage**: Creates the final lightweight image for production use

This ensures that only images that pass tests are deployed to production.

## 📦 Dependency Management

The project uses uv exclusively for dependency management, with all dependencies defined in `pyproject.toml`.

### Installing Dependencies with uv

```bash
# Install core package with all dependencies
uv sync --all-groups

# Install with specific groups
uv sync --group main  # Main dependencies only (for CLI)
uv sync --group dev   # Development dependencies
uv sync --group test  # Test dependencies
uv sync --group api   # API dependencies
```

## 🧹 Cleanup

To reset your environment:

```bash
./scripts/cleanup.sh
```

This will remove all local environments and stop Docker containers (data files will not be affected).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 