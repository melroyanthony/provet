"""Main application module implementing the Facade design pattern.

This module provides a high-level interface for the application, hiding the
complexity of the underlying components.
"""

from pathlib import Path

from provet.core.io_manager import IOManager
from provet.core.llm_service import create_llm_service
from provet.utils.template_engine import TemplateEngine


class DischargeNoteGenerator:
    """Main application class implementing the Facade design pattern.

    This class provides a simple interface to the application's functionality,
    hiding the complexity of the underlying components.

    Attributes:
        io_manager: Manager for file I/O operations.
        llm_service: Service for interacting with language models.
        template_engine: Engine for rendering templates.
    """

    def __init__(self) -> None:
        """Initialize the discharge note generator."""
        self.template_engine = TemplateEngine()
        self.llm_service = create_llm_service(self.template_engine)
        self.io_manager = IOManager()

    def process_file(self, file_path: str | Path) -> str:
        """Process a consultation data file and generate a discharge note.

        Args:
            file_path: Path to the JSON file containing consultation data.

        Returns:
            Path to the saved discharge note file.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If there's an error processing the file.
        """
        try:
            # Load consultation data
            consultation_data = self.io_manager.load_consultation_data(file_path)

            # Generate template context
            context = consultation_data.to_template_context()

            # Generate discharge note
            discharge_note = self.llm_service.generate_discharge_note(context)

            # Save discharge note
            output_path = self.io_manager.save_discharge_note(discharge_note, file_path)

            return str(output_path)
        except Exception as e:
            raise ValueError(f"❌ Error processing file {file_path}: {e}")


# Factory function to create DischargeNoteGenerator instances
def create_discharge_note_generator() -> DischargeNoteGenerator:
    """Create a new DischargeNoteGenerator instance.

    Returns:
        New DischargeNoteGenerator instance.
    """
    return DischargeNoteGenerator()
