"""LLM service for generating discharge notes.

This module provides a multi-provider service for interacting with language models
(OpenAI, Anthropic) to generate discharge notes based on consultation data.
"""

from typing import Any

import anthropic
import openai

from provet.core.guardrails import PHIRedactor
from provet.utils.config import config_manager
from provet.utils.template_engine import TemplateEngine


class LLMService:
    """Service for interacting with Language Models.

    Supports OpenAI and Anthropic providers. The provider is selected via the
    LLM_PROVIDER environment variable (default: openai).

    Attributes:
        provider: The LLM provider name ("openai" or "anthropic").
        client: Provider-specific client instance.
        template_engine: Template engine for rendering prompts.
        phi_redactor: PHI redaction guardrail (enabled by default).
    """

    def __init__(self, template_engine: TemplateEngine | None = None) -> None:
        """Initialize the LLM service.

        Args:
            template_engine: Template engine instance for rendering prompts.
                If not provided, a new instance will be created.
        """
        self.provider = config_manager.get("provider")
        self.template_engine = template_engine or TemplateEngine()
        self.phi_redactor = PHIRedactor(
            enabled=config_manager.get("enable_phi_redaction", True)
        )

        if self.provider == "anthropic":
            self.client = anthropic.Anthropic(
                api_key=config_manager.get("api_key")
            )
        else:
            self.client = openai.OpenAI(
                api_key=config_manager.get("api_key")
            )

    def generate_discharge_note(self, context: dict[str, Any]) -> str:
        """Generate a discharge note based on consultation data.

        Applies PHI redaction before sending to the LLM and restores
        original values in the response.

        Args:
            context: Dictionary containing template context data.

        Returns:
            Generated discharge note as a string.

        Raises:
            Exception: If there's an error generating the note.
        """
        try:
            context["custom_instruction"] = config_manager.get("custom_instruction", "")

            system_message = self.template_engine.render_template(
                "system_message.j2", context
            )
            prompt = self.template_engine.render_template(
                "discharge_prompt.j2", context
            )

            # Redact PHI before sending to LLM
            redacted_prompt, mapping = self.phi_redactor.redact(prompt)

            if self.provider == "anthropic":
                raw = self._call_anthropic(system_message, redacted_prompt)
            else:
                raw = self._call_openai(system_message, redacted_prompt)

            # Restore original PHI values in the response
            return self.phi_redactor.restore(raw, mapping)
        except Exception as e:
            raise Exception(f"Error generating discharge note: {e}")

    def _call_openai(self, system_message: str, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=config_manager.get("model"),
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            temperature=config_manager.get("temperature"),
            max_tokens=config_manager.get("max_tokens"),
        )
        return response.choices[0].message.content.strip()

    def _call_anthropic(self, system_message: str, prompt: str) -> str:
        response = self.client.messages.create(
            model=config_manager.get("model"),
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
            temperature=config_manager.get("temperature"),
            max_tokens=config_manager.get("max_tokens"),
        )
        return response.content[0].text.strip()


def create_llm_service(template_engine: TemplateEngine | None = None) -> LLMService:
    """Create a new LLMService instance.

    Args:
        template_engine: Optional template engine to use.

    Returns:
        New LLMService instance.
    """
    return LLMService(template_engine)
