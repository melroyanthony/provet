"""Input/Output manager for file operations.

This module provides functionality for loading consultation data from files
and saving discharge notes to files.
"""

import json
from pathlib import Path

from provet.core.data_models import ConsultationData
from provet.utils.config import config_manager


class IOManager:
    """Handles file input/output operations.

    This class provides methods for loading consultation data from files and
    saving discharge notes to files.
    """

    @staticmethod
    def load_consultation_data(file_path: str | Path) -> ConsultationData:
        """Load consultation data from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            ConsultationData object containing the loaded data.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file contains invalid JSON or is missing required data.
        """
        path = Path(file_path)
        try:
            with path.open("r") as f:
                raw_data = json.load(f)
            return ConsultationData.from_dict(raw_data)
        except FileNotFoundError:
            raise FileNotFoundError(f"🔍 File {file_path} not found.")
        except json.JSONDecodeError:
            raise ValueError(f"📋 File {file_path} contains invalid JSON.")
        except Exception as e:
            raise ValueError(f"❌ Error loading consultation data: {e}")

    @staticmethod
    def save_discharge_note(
        discharge_note: str,
        input_file: str | Path,
        output_dir: str | Path | None = None,
    ) -> Path:
        """Save a discharge note as a JSON file.

        Args:
            discharge_note: The generated discharge note.
            input_file: Path to the input file, used to determine the output filename.
            output_dir: Directory to save the output file. If not provided,
                uses the default from config.

        Returns:
            Path to the saved file.

        Raises:
            ValueError: If there's an error saving the file.
        """
        # Create the output JSON
        output_data = {"discharge_note": discharge_note}

        # Determine the output path
        input_path = Path(input_file)
        output_dir = Path(output_dir or config_manager.get("solution_dir"))
        output_path = output_dir / f"{input_path.stem}_discharge.json"

        # Create the output directory if it doesn't exist
        output_dir.mkdir(exist_ok=True)

        # Save the output
        try:
            with output_path.open("w") as f:
                json.dump(output_data, f, indent=4)
            return output_path
        except Exception as e:
            raise ValueError(f"❌ Error saving discharge note: {e}")
