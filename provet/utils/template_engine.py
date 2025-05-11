"""Template engine utilities.

This module provides functionality for working with Jinja2 templates, including
rendering templates with context data.
"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template

from provet.utils.config import config_manager


class TemplateEngine:
    """Template rendering engine using Jinja2.

    This class handles loading and rendering of Jinja2 templates with
    provided context data.

    Attributes:
        env (Environment): Jinja2 environment for template processing.
    """

    def __init__(self, templates_dir: Path | None = None) -> None:
        """Initialize the template engine.

        Args:
            templates_dir: Directory containing template files.
                If not provided, uses default from config.
        """
        self.templates_dir = templates_dir or config_manager.get("templates_dir")
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

    def get_template(self, template_name: str) -> Template:
        """Get a Jinja2 template by name.

        Args:
            template_name: Name of the template file.

        Returns:
            The loaded Jinja2 template.

        Raises:
            TemplateNotFound: If the template doesn't exist.
        """
        return self.env.get_template(template_name)

    def render_template(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a template with the provided context.

        Args:
            template_name: Name of the template file.
            context: Dictionary containing context data for template rendering.

        Returns:
            The rendered template as a string.

        Raises:
            TemplateNotFound: If the template doesn't exist.
            TemplateError: If there's an error during rendering.
        """
        template = self.get_template(template_name)
        return template.render(**context)

    def update_templates_dir(self, templates_dir: Path) -> None:
        """Update the templates directory.

        Args:
            templates_dir: New directory containing template files.

        Raises:
            ValueError: If the directory doesn't exist.
        """
        if not templates_dir.is_dir():
            raise ValueError(f"Template directory {templates_dir} does not exist.")

        self.templates_dir = templates_dir
        self.env = Environment(loader=FileSystemLoader(templates_dir))
