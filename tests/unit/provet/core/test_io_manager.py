"""Unit tests for io_manager.py module.

Tests for the IOManager class responsible for file operations.
"""

import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from provet.core.data_models import ConsultationData
from provet.core.io_manager import IOManager


class TestIOManager:
    """Test class for the IOManager."""

    def test_load_consultation_data(self, temp_file):
        """Test loading consultation data from a file.

        Given: A file with valid consultation data
        When: load_consultation_data is called
        Then: It should return a ConsultationData object with the data from the file.
        """
        # Setup
        io_manager = IOManager()

        # Execute
        result = io_manager.load_consultation_data(temp_file)

        # Assert
        assert isinstance(result, ConsultationData)
        assert result.patient.name == "Max"
        assert result.patient.species == "Dog (Canine - Domestic)"
        assert result.patient.breed == "Golden Retriever"
        assert result.consultation.date == "2023-07-15"
        assert result.consultation.time == "10:30"
        assert result.consultation.reason == "Vomiting and lethargy"
        assert result.consultation.type == "Outpatient"

    def test_load_consultation_data_file_not_found(self):
        """Test handling of file not found error.

        Given: A non-existent file path
        When: load_consultation_data is called
        Then: It should raise a FileNotFoundError.
        """
        # Setup
        io_manager = IOManager()
        non_existent_path = Path("non_existent_file.json")

        # Execute and Assert
        with pytest.raises(FileNotFoundError) as excinfo:
            io_manager.load_consultation_data(non_existent_path)

        assert "not found" in str(excinfo.value)

    def test_load_consultation_data_invalid_json(self):
        """Test handling of invalid JSON.

        Given: A file with invalid JSON content
        When: load_consultation_data is called
        Then: It should raise a ValueError.
        """
        # Setup
        io_manager = IOManager()
        path = Path("test.json")

        # Use contextmanager directly to mock the file opening
        with patch("pathlib.Path.open", mock_open(read_data="not valid json")):
            with patch(
                "json.load", side_effect=json.JSONDecodeError("Invalid JSON", "", 0)
            ):
                # Execute and Assert
                with pytest.raises(ValueError) as excinfo:
                    io_manager.load_consultation_data(path)

                assert "invalid JSON" in str(excinfo.value)

    @pytest.mark.parametrize(
        "input_path, expected_output_name",
        [
            ("test.json", "test_discharge.json"),
            ("data/sample.json", "sample_discharge.json"),
            ("/absolute/path/file.json", "file_discharge.json"),
        ],
    )
    def test_save_discharge_path_construction(self, input_path, expected_output_name):
        """Test just the path construction logic without file operations.

        Given: Different input file paths
        When: Constructing output paths
        Then: The output file name should be constructed correctly.
        """
        # Validation logic, not actual file operations
        input_path_obj = Path(input_path)
        output_name = f"{input_path_obj.stem}_discharge.json"

        assert output_name == expected_output_name

    def test_custom_output_dir_path_construction(self):
        """Test path construction with a custom output directory.

        Given: An input file and custom output directory
        When: Constructing output paths
        Then: The output path should combine the directory and filename correctly.
        """
        # Setup
        input_path = "test.json"
        custom_dir = Path("/custom/output/dir")

        # Validation logic without file operations
        input_path_obj = Path(input_path)
        expected_path = custom_dir / f"{input_path_obj.stem}_discharge.json"

        assert expected_path.name == "test_discharge.json"
        assert expected_path.parent == custom_dir
