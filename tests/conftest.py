"""Pytest configuration and shared fixtures.

This module provides fixtures that can be shared across all test modules.
"""

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from provet.core.data_models import ConsultationData
from provet.utils.template_engine import TemplateEngine


@pytest.fixture
def sample_consultation_data() -> dict[str, Any]:
    """Create a sample dictionary of consultation data for testing.

    Returns:
        Dictionary containing sample consultation data.
    """
    return {
        "patient": {
            "name": "Max",
            "species": "Dog (Canine - Domestic)",
            "breed": "Golden Retriever",
            "gender": "Male",
            "neutered": True,
            "date_of_birth": "2018-05-10",
            "weight": "32 kg",
            "microchip": "123456789012345",
        },
        "consultation": {
            "date": "2023-07-15",
            "time": "10:30",
            "reason": "Vomiting and lethargy",
            "type": "Outpatient",
            "clinical_notes": [
                {
                    "note": "Patient presented with vomiting and lethargy for the past 24 hours.",
                    "type": "general",
                },
                {
                    "note": "Suspected gastroenteritis based on symptoms and examination.",
                    "type": "assessment",
                },
            ],
            "treatment_items": {
                "procedures": [
                    {
                        "name": "Physical examination",
                        "date": "2023-07-15",
                        "time": "10:35",
                    },
                    {"name": "Blood test", "date": "2023-07-15", "time": "10:45"},
                ],
                "medicines": [
                    {
                        "name": "Cerenia",
                        "dosage": "2 mg/kg",
                        "instructions": "Administered subcutaneously",
                    }
                ],
                "prescriptions": [
                    {
                        "name": "Metronidazole",
                        "dosage": "10 mg/kg twice daily",
                        "instructions": "Give with food",
                        "duration": "5 days",
                    }
                ],
                "foods": [],
                "supplies": [],
            },
            "diagnostics": [
                {
                    "name": "Complete Blood Count",
                    "result": "Within normal limits",
                    "notes": "No significant abnormalities detected",
                }
            ],
        },
    }


@pytest.fixture
def consultation_data_object(sample_consultation_data) -> ConsultationData:
    """Create a ConsultationData object for testing.

    Args:
        sample_consultation_data: Dictionary fixture with sample data.

    Returns:
        ConsultationData object populated with sample data.
    """
    return ConsultationData.from_dict(sample_consultation_data)


@pytest.fixture
def mock_template_engine() -> MagicMock:
    """Create a mock template engine.

    Returns:
        MagicMock object mocking TemplateEngine.
    """
    mock = MagicMock(spec=TemplateEngine)
    mock.render_template.return_value = "Test template rendering"
    return mock


@pytest.fixture
def mock_openai_response() -> MagicMock:
    """Create a mock OpenAI API response.

    Returns:
        MagicMock object simulating an OpenAI API response.
    """
    mock_message = MagicMock()
    mock_message.content = "This is a test discharge note."

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    return mock_response


@pytest.fixture
def temp_file(tmp_path) -> Path:
    """Create a temporary file with sample consultation data.

    Args:
        tmp_path: Pytest fixture providing a temporary directory.

    Returns:
        Path to the temporary file.
    """
    file_path = tmp_path / "test_consultation.json"
    with open(file_path, "w") as f:
        json.dump(
            {
                "patient": {
                    "name": "Max",
                    "species": "Dog (Canine - Domestic)",
                    "breed": "Golden Retriever",
                    "gender": "Male",
                    "neutered": True,
                    "date_of_birth": "2018-05-10",
                    "weight": "32 kg",
                },
                "consultation": {
                    "date": "2023-07-15",
                    "time": "10:30",
                    "reason": "Vomiting and lethargy",
                    "type": "Outpatient",
                    "clinical_notes": [],
                },
            },
            f,
        )
    return file_path
