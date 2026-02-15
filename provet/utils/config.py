"""Configuration management utilities.

This module provides functionality to load and manage configuration settings
from environment variables and other sources.
"""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


class ConfigurationManager:
    """Manages application configuration settings.

    This class is responsible for loading configuration from environment variables
    and providing access to those settings throughout the application.

    Attributes:
        config (Dict[str, Any]): Dictionary containing configuration settings.
    """

    def __init__(self) -> None:
        """Initialize the configuration manager and load settings."""
        # Load environment variables from .env file
        load_dotenv()

        provider = os.getenv("LLM_PROVIDER", "openai").lower()

        # Initialize config dictionary
        self.config: dict[str, Any] = {
            # Provider selection
            "provider": provider,
            # OpenAI configuration
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "openai_model": os.getenv("OPENAI_MODEL", "gpt-4o"),
            # Anthropic configuration
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
            "anthropic_model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929"),
            # Shared LLM configuration
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("MAX_TOKENS", "800")),
            # PHI redaction guardrails
            "enable_phi_redaction": os.getenv("ENABLE_PHI_REDACTION", "true").lower() == "true",
            # Custom instructions
            "custom_instruction": os.getenv("CUSTOM_SYSTEM_INSTRUCTION", ""),
            # Default paths
            "templates_dir": Path(__file__).parent.parent / "templates",
            "solution_dir": Path("solution"),
        }

        # Backwards compatibility: map old OPENAI_API_KEY to provider-specific key
        if os.getenv("OPENAI_API_KEY") and not os.getenv("LLM_PROVIDER"):
            self.config["provider"] = "openai"

        # Validate necessary configuration
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate required configuration settings.

        Raises:
            ValueError: If required configuration values are missing.
        """
        provider = self.config["provider"]
        if provider == "openai" and not self.config.get("openai_api_key"):
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it in your environment or create a .env file."
            )
        if provider == "anthropic" and not self.config.get("anthropic_api_key"):
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is not set. "
                "Please set it in your environment or create a .env file."
            )

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: The configuration key to retrieve.
            default: Default value to return if the key doesn't exist.

        Returns:
            The configuration value or the default if not found.
        """
        # Backwards compatibility: map old keys to new provider-specific keys
        if key == "api_key":
            provider = self.config["provider"]
            return self.config.get(f"{provider}_api_key", default)
        if key == "model":
            provider = self.config["provider"]
            return self.config.get(f"{provider}_model", default)
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: The configuration key to set.
            value: The value to assign to the key.
        """
        self.config[key] = value

    def update(self, new_config: dict[str, Any]) -> None:
        """Update multiple configuration values.

        Args:
            new_config: Dictionary containing configuration values to update.
        """
        self.config.update(new_config)


# Create a singleton instance for global access
config_manager = ConfigurationManager()
