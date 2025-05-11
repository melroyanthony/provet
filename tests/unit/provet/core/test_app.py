"""Unit tests for app.py module.

Tests for the DischargeNoteGenerator class and related functionality.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from provet.core.app import DischargeNoteGenerator, create_discharge_note_generator
from provet.core.data_models import ConsultationData


class TestDischargeNoteGenerator:
    """Test class for the DischargeNoteGenerator."""

    def test_init(self):
        """Test initialization of the DischargeNoteGenerator.

        Given: No specific inputs
        When: A DischargeNoteGenerator instance is created
        Then: It should have the expected attributes properly initialized.
        """
        with patch("provet.core.app.create_llm_service") as mock_create_llm_service:
            mock_llm_service = MagicMock()
            mock_create_llm_service.return_value = mock_llm_service

            # Execute
            generator = DischargeNoteGenerator()

            # Assert
            assert generator.llm_service == mock_llm_service
            assert generator.template_engine is not None
            assert generator.io_manager is not None

    def test_update_template_dir(self):
        """Test updating the template directory.

        Given: A DischargeNoteGenerator instance and a new template directory
        When: update_template_dir is called
        Then: It should update the template directory in the template engine.
        """
        # Setup
        generator = DischargeNoteGenerator()
        generator.template_engine = MagicMock()
        new_templates_dir = Path("/new/templates/dir")

        # Execute
        generator.update_template_dir(new_templates_dir)

        # Assert
        generator.template_engine.update_templates_dir.assert_called_once_with(
            new_templates_dir
        )

    @pytest.mark.parametrize(
        "context, discharge_note",
        [
            ({"patient": {"name": "Max"}}, "Simple discharge note"),
            (
                {
                    "patient": {"name": "Luna"},
                    "clinical_notes": [{"note": "Test note"}],
                },
                "Complex discharge note",
            ),
        ],
    )
    def test_process_file(self, context, discharge_note, tmp_path):
        """Test processing a file to generate a discharge note.

        Given: Different consultation data contexts and expected discharge notes
        When: process_file is called
        Then: It should load the data, generate the note, and save it to the expected path.
        """
        # Setup
        generator = DischargeNoteGenerator()

        # Mock IO manager
        generator.io_manager = MagicMock()
        mock_consultation_data = MagicMock(spec=ConsultationData)
        mock_consultation_data.to_template_context.return_value = context
        generator.io_manager.load_consultation_data.return_value = (
            mock_consultation_data
        )
        generator.io_manager.save_discharge_note.return_value = str(
            tmp_path / "output.json"
        )

        # Mock LLM service
        generator.llm_service = MagicMock()
        generator.llm_service.generate_discharge_note.return_value = discharge_note

        # Execute
        result = generator.process_file("test.json")

        # Assert
        generator.io_manager.load_consultation_data.assert_called_once_with("test.json")
        mock_consultation_data.to_template_context.assert_called_once()
        generator.llm_service.generate_discharge_note.assert_called_once_with(context)
        generator.io_manager.save_discharge_note.assert_called_once_with(
            discharge_note, "test.json"
        )
        assert result == str(tmp_path / "output.json")

    def test_process_file_error(self):
        """Test error handling when processing a file.

        Given: A DischargeNoteGenerator instance and a process that raises an exception
        When: process_file is called
        Then: It should catch the exception and raise a ValueError with details.
        """
        # Setup
        generator = DischargeNoteGenerator()
        generator.io_manager = MagicMock()
        generator.io_manager.load_consultation_data.side_effect = Exception(
            "Test error"
        )

        # Execute and Assert
        with pytest.raises(ValueError) as excinfo:
            generator.process_file("test.json")

        assert "Error processing file" in str(excinfo.value)
        assert "Test error" in str(excinfo.value)

    def test_create_discharge_note_generator(self):
        """Test the factory function for creating DischargeNoteGenerator instances.

        Given: No specific inputs
        When: create_discharge_note_generator is called
        Then: It should return a properly configured DischargeNoteGenerator instance.
        """
        # Execute
        generator = create_discharge_note_generator()

        # Assert
        assert isinstance(generator, DischargeNoteGenerator)
        assert generator.template_engine is not None
        assert generator.llm_service is not None
        assert generator.io_manager is not None
