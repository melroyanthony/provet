"""LLM service for generating discharge notes.

This module provides a service for interacting with language models to generate
discharge notes based on consultation data.
"""

from typing import Any

import openai

from provet.utils.config import config_manager
from provet.utils.template_engine import TemplateEngine


class LLMService:
    """Service for interacting with Language Models.

    This class provides functionality to generate discharge notes using
    OpenAI's language models.

    Attributes:
        client: OpenAI client instance.
        template_engine: Template engine for rendering prompts.
    """

    def __init__(self, template_engine: TemplateEngine | None = None) -> None:
        """Initialize the LLM service.

        Args:
            template_engine: Template engine instance for rendering prompts.
                If not provided, a new instance will be created.
        """
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=config_manager.get("api_key"))

        # Initialize template engine
        self.template_engine = template_engine or TemplateEngine()

    def generate_discharge_note(self, context: dict[str, Any]) -> str:
        """Generate a discharge note based on consultation data.

        Args:
            context: Dictionary containing template context data.

        Returns:
            Generated discharge note as a string.

        Raises:
            Exception: If there's an error generating the note.
        """
        try:
            # Add custom instruction to context if it exists
            context["custom_instruction"] = config_manager.get("custom_instruction", "")

            # Render templates
            system_message = self.template_engine.render_template(
                "system_message.j2", context
            )
            prompt = self.template_engine.render_template(
                "discharge_prompt.j2", context
            )

            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=config_manager.get("model"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=config_manager.get("temperature"),
                max_tokens=config_manager.get("max_tokens"),
            )

            # Extract and return the generated note
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating discharge note: {e}")


# Factory function to create LLMService instances
def create_llm_service(template_engine: TemplateEngine | None = None) -> LLMService:
    """Create a new LLMService instance.

    Args:
        template_engine: Optional template engine to use.

    Returns:
        New LLMService instance.
    """
    return LLMService(template_engine)
