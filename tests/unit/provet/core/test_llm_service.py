"""Unit tests for llm_service.py module.

Tests for the LLMService class with mocked OpenAI calls.
"""

from unittest.mock import MagicMock, patch

import pytest

from provet.core.llm_service import LLMService, create_llm_service
from provet.utils.template_engine import TemplateEngine


class TestLLMService:
    """Test class for the LLMService."""

    @patch("openai.OpenAI")
    def test_llm_service_init(self, mock_openai_class):
        """Test LLMService initialization.

        Given: An OpenAI API key in config
        When: A LLMService instance is created
        Then: The OpenAI client should be initialized with the API key.
        """
        # Setup
        mock_openai_instance = MagicMock()
        mock_openai_class.return_value = mock_openai_instance

        # Execute
        service = LLMService()

        # Assert
        assert service.client == mock_openai_instance
        assert mock_openai_class.called

    @patch("openai.OpenAI")
    def test_llm_service_init_with_template_engine(self, mock_openai_class):
        """Test LLMService initialization with a provided template engine.

        Given: A template engine instance
        When: A LLMService instance is created with the template engine
        Then: The service should use the provided template engine.
        """
        # Setup
        mock_template_engine = MagicMock(spec=TemplateEngine)

        # Execute
        service = LLMService(template_engine=mock_template_engine)

        # Assert
        assert service.template_engine == mock_template_engine

    @patch("openai.OpenAI")
    def test_generate_discharge_note(
        self, mock_openai_class, mock_template_engine, mock_openai_response
    ):
        """Test generate_discharge_note method.

        Given: A context dictionary and mocked OpenAI response
        When: generate_discharge_note is called
        Then: It should render templates, call the OpenAI API, and return the generated note.
        """
        # Setup
        mock_openai_instance = MagicMock()
        mock_openai_class.return_value = mock_openai_instance

        MagicMock()
        mock_openai_instance.chat.completions.create.return_value = mock_openai_response

        context = {"patient": {"name": "Max"}, "consultation": {"reason": "Checkup"}}

        mock_template_engine.render_template.side_effect = [
            "System message for test",
            "User prompt for test",
        ]

        service = LLMService(template_engine=mock_template_engine)

        # Execute
        result = service.generate_discharge_note(context)

        # Assert
        assert mock_template_engine.render_template.call_count == 2
        mock_template_engine.render_template.assert_any_call(
            "system_message.j2", context
        )
        mock_template_engine.render_template.assert_any_call(
            "discharge_prompt.j2", context
        )

        mock_openai_instance.chat.completions.create.assert_called_once()
        assert result == "This is a test discharge note."

    @pytest.mark.parametrize(
        "context",
        [
            {"patient": {"name": "Max"}, "consultation": {"reason": "Checkup"}},
            {"patient": {"name": "Luna"}, "consultation": {"reason": "Vaccination"}},
            {"patient": {"name": "Buddy"}, "consultation": {"reason": "Injury"}},
        ],
    )
    @patch("openai.OpenAI")
    def test_generate_discharge_note_parametrized(
        self, mock_openai_class, mock_template_engine, mock_openai_response, context
    ):
        """Test generate_discharge_note with different contexts.

        Given: Various context dictionaries and mocked OpenAI responses
        When: generate_discharge_note is called
        Then: It should correctly process each context.
        """
        # Setup
        mock_openai_instance = MagicMock()
        mock_openai_class.return_value = mock_openai_instance
        mock_openai_instance.chat.completions.create.return_value = mock_openai_response

        service = LLMService(template_engine=mock_template_engine)

        # Execute
        result = service.generate_discharge_note(context)

        # Assert
        assert result == "This is a test discharge note."
        # Verify custom instruction was added to context
        assert "custom_instruction" in context

    @patch("openai.OpenAI")
    def test_generate_discharge_note_error(
        self, mock_openai_class, mock_template_engine
    ):
        """Test generate_discharge_note handling of errors.

        Given: A context and OpenAI API that raises an exception
        When: generate_discharge_note is called
        Then: It should raise an exception with an appropriate message.
        """
        # Setup
        mock_openai_instance = MagicMock()
        mock_openai_class.return_value = mock_openai_instance
        mock_openai_instance.chat.completions.create.side_effect = Exception(
            "API error"
        )

        service = LLMService(template_engine=mock_template_engine)
        context = {"patient": {"name": "Max"}}

        # Execute and Assert
        with pytest.raises(Exception) as excinfo:
            service.generate_discharge_note(context)

        assert "Error generating discharge note" in str(excinfo.value)

    def test_create_llm_service(self, mock_template_engine):
        """Test create_llm_service factory function.

        Given: A template engine
        When: create_llm_service is called
        Then: It should return a properly configured LLMService instance.
        """
        with patch("openai.OpenAI"):
            # Execute
            service = create_llm_service(mock_template_engine)

            # Assert
            assert isinstance(service, LLMService)
            assert service.template_engine == mock_template_engine
