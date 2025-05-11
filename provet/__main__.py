#!/usr/bin/env python3
"""Command-line interface for Provet Cloud Discharge Note Generator.

This module provides the main entry point for the application when executed
from the command line.
"""

import argparse
import sys
from pathlib import Path

from provet.core.app import create_discharge_note_generator


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="Generate a discharge note from consultation data."
    )
    parser.add_argument(
        "file", help="Path to a JSON file containing consultation data."
    )
    parser.add_argument(
        "--template-dir",
        help="Directory containing Jinja2 templates (default: ./templates)",
        type=Path,
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save the output file (default: ./solution)",
        type=Path,
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point function.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    args = parse_args()

    try:
        # Create discharge note generator
        generator = create_discharge_note_generator()

        # Update template directory if provided
        if args.template_dir:
            generator.update_template_dir(args.template_dir)

        # Process file
        output_path = generator.process_file(args.file)

        print(f"✅ Discharge note successfully generated and saved to {output_path} 📄")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
