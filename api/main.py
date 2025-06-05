"""FastAPI service for Provet Cloud Discharge Note Generator.

This module provides a REST API for the Provet application, allowing clients to
generate discharge notes via HTTP requests.
"""

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from provet.core.app import create_discharge_note_generator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Provet API",
    description="API for generating veterinary discharge notes",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, limit this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Provet generator
discharge_generator = create_discharge_note_generator()

# Create temporary directory for file uploads
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class ConsultationRequest(BaseModel):
    """Request model for consultation data."""

    consultation_data: dict[str, Any] = Field(
        ..., description="JSON consultation data for discharge note generation"
    )


class DischargeNoteResponse(BaseModel):
    """Response model for discharge notes."""

    discharge_note: str = Field(..., description="Generated discharge note")


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Dictionary with status message.
    """
    return {"status": "✅ API is up and running"}


@app.post("/generate", response_model=DischargeNoteResponse)
async def generate_discharge_note(
    request: ConsultationRequest,
) -> DischargeNoteResponse:
    """Generate a discharge note from consultation data.

    Args:
        request: Consultation data for discharge note generation.

    Returns:
        DischargeNoteResponse containing the generated discharge note.

    Raises:
        HTTPException: If there's an error generating the discharge note.
    """
    try:
        logger.info("🔍 Received request to generate discharge note")

        # Create a temp file to store the consultation data
        temp_file = UPLOAD_DIR / f"consultation_{id(request)}.json"
        output_path: Path | None = None
        try:
            with temp_file.open("w") as f:
                json.dump(request.consultation_data, f)

            # Process the file with the discharge note generator
            output_path = discharge_generator.process_file(temp_file)

            # Read the generated discharge note
            output_path = Path(output_path)
            with output_path.open("r") as f:
                output_data = json.load(f)

            return DischargeNoteResponse(discharge_note=output_data["discharge_note"])
        finally:
            # Clean up temporary files
            if temp_file.exists():
                temp_file.unlink()
            if output_path and output_path.exists():
                output_path.unlink()

    except Exception as e:
        logger.error(f"❌ Error generating discharge note: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload", response_model=DischargeNoteResponse)
async def upload_consultation_file(
    file: UploadFile = File(...), background_tasks: BackgroundTasks = None
) -> DischargeNoteResponse:
    """Generate a discharge note from an uploaded JSON file.

    Args:
        file: Uploaded JSON file containing consultation data.
        background_tasks: Background tasks for cleanup.

    Returns:
        DischargeNoteResponse containing the generated discharge note.

    Raises:
        HTTPException: If there's an error generating the discharge note.
    """
    try:
        logger.info(f"📤 Received file upload: {file.filename}")

        # Ensure the file is JSON
        if not file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="Only JSON files are supported")

        # Save the uploaded file
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as f:
            content = await file.read()
            f.write(content)

        # Process the file with the discharge note generator
        output_path = discharge_generator.process_file(file_path)

        # Read the generated discharge note
        output_path = Path(output_path)
        with output_path.open("r") as f:
            output_data = json.load(f)

        # Add cleanup to background tasks
        if background_tasks:
            background_tasks.add_task(cleanup_files, file_path, output_path)

        return DischargeNoteResponse(discharge_note=output_data["discharge_note"])

    except Exception as e:
        logger.error(f"❌ Error processing uploaded file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def cleanup_files(input_path: Path, output_path: Path) -> None:
    """Clean up temporary files.

    Args:
        input_path: Path to the input file.
        output_path: Path to the output file.
    """
    try:
        if input_path.exists():
            input_path.unlink()
        if output_path.exists():
            output_path.unlink()
    except Exception as e:
        logger.error(f"❌ Error cleaning up files: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
