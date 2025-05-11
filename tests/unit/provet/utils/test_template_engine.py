"""Unit tests for template_engine.py module.

Tests for the TemplateEngine class that handles Jinja2 templates.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from jinja2 import Template, TemplateNotFound

from provet.utils.template_engine import TemplateEngine


class TestTemplateEngine:
    """Test class for the TemplateEngine."""

    @patch("provet.utils.config.config_manager.get")
    @patch("provet.utils.template_engine.Environment")
    def test_init_default_dir(self, mock_environment, mock_get, tmp_path):
        """Test initialization with the default templates directory.

        Given: No specific template directory
        When: A TemplateEngine instance is created
        Then: It should use the default directory from config.
        """
        # Setup
        default_dir = tmp_path / "default_templates"
        mock_get.return_value = default_dir
        mock_env = MagicMock()
        mock_environment.return_value = mock_env

        # Execute
        engine = TemplateEngine()

        # Assert
        assert engine.templates_dir == default_dir
        mock_environment.assert_called_once()

    def test_get_template(self):
        """Test getting a template by name.

        Given: A template name
        When: get_template is called
        Then: It should return the appropriate Jinja2 template.
        """
        # Setup
        engine = TemplateEngine()
        mock_template = MagicMock(spec=Template)
        engine.env = MagicMock()
        engine.env.get_template.return_value = mock_template

        # Execute
        result = engine.get_template("test_template.j2")

        # Assert
        assert result == mock_template
        engine.env.get_template.assert_called_once_with("test_template.j2")

    def test_get_template_not_found(self):
        """Test error handling when a template is not found.

        Given: A non-existent template name
        When: get_template is called
        Then: It should raise a TemplateNotFound exception.
        """
        # Setup
        engine = TemplateEngine()
        engine.env = MagicMock()
        engine.env.get_template.side_effect = TemplateNotFound("test_template.j2")

        # Execute and Assert
        with pytest.raises(TemplateNotFound):
            engine.get_template("test_template.j2")

    @pytest.mark.parametrize(
        "template_name, context, expected_result",
        [
            ("basic.j2", {"name": "Test"}, "Hello, Test!"),
            ("complex.j2", {"items": [1, 2, 3]}, "Items: 1, 2, 3"),
        ],
    )
    def test_render_template(self, template_name, context, expected_result):
        """Test rendering a template with context data.

        Given: Different templates and context data
        When: render_template is called
        Then: It should render the template with the provided context.
        """
        # Setup
        engine = TemplateEngine()
        mock_template = MagicMock(spec=Template)
        mock_template.render.return_value = expected_result
        engine.get_template = MagicMock(return_value=mock_template)

        # Execute
        result = engine.render_template(template_name, context)

        # Assert
        assert result == expected_result
        engine.get_template.assert_called_once_with(template_name)
        mock_template.render.assert_called_once_with(**context)
