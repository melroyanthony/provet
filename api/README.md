# Provet Cloud API

![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-blue)
![Python](https://img.shields.io/badge/Python-3.13%2B-green)
![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen)

This service provides a REST API for the Provet Cloud Discharge Note Generator, allowing seamless integration with existing veterinary practice management systems.

## ✨ Features

- 🔄 **RESTful API**: Built using FastAPI for high performance
- 📝 **Note Generation**: Generate discharge notes from JSON consultation data
- 📤 **File Upload**: Support for JSON file uploads
- 📚 **Swagger Documentation**: Interactive API documentation via Swagger UI
- 🔍 **Validation**: Automatic validation of input data
- 🐳 **Docker Ready**: Easily deploy with Docker or Docker Compose

## 🛣️ Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check endpoint |
| `POST` | `/generate` | Generate discharge note from JSON data |
| `POST` | `/upload` | Upload JSON file for processing |
| `GET` | `/docs` | Swagger UI documentation |

## 🚀 Running the API

### Using Docker

Build and run the Docker container:

```bash
docker build -t provet-api .
docker run -p 8000:8000 --env-file .env provet-api
```

### Using Docker Compose

```bash
docker-compose up -d
```

### Local Development

Setup the development environment:

```bash
# Create development environment
./scripts/setup_dev.sh

# Activate environment
source .venv/bin/activate
```

Run the API with hot-reloading:

```bash
python -m uvicorn api.main:app --reload
```

## 💻 API Usage Examples

### Generate Discharge Note

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "consultation_data": {
      "patient": {
        "name": "Sparky",
        "species": "Dog (Canine - Domestic)",
        "breed": "Terrier - Parson Russel",
        "gender": "male",
        "neutered": true,
        "date_of_birth": "2023-02-28",
        "microchip": "1234567890",
        "weight": "8 kg"
      },
      "consultation": {
        "date": "2025-03-19",
        "time": "09:15",
        "reason": "Ophtho | Eyelid Mass Removal",
        "type": "Outpatient",
        "clinical_notes": [],
        "treatment_items": {
          "procedures": [],
          "medicines": [],
          "prescriptions": [],
          "foods": [],
          "supplies": []
        },
        "diagnostics": []
      }
    }
  }'
```

### Upload File

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/consultation1.json"
```

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `OPENAI_MODEL` | OpenAI model name | `gpt-4o` |
| `TEMPERATURE` | Temperature for text generation | `0.7` |
| `MAX_TOKENS` | Maximum tokens for generated text | `800` |
| `CUSTOM_SYSTEM_INSTRUCTION` | Custom system instructions for the LLM | - |

## 📚 Related Resources

- [Main Project README](../README.md)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [FastAPI Documentation](https://fastapi.tiangolo.com/) 