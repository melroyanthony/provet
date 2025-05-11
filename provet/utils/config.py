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

        # Initialize config dictionary
        self.config: dict[str, Any] = {
            # API configuration
            "api_key": os.getenv("OPENAI_API_KEY"),
            # LLM configuration
            "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("MAX_TOKENS", "800")),
            # Custom instructions
            "custom_instruction": os.getenv("CUSTOM_SYSTEM_INSTRUCTION", ""),
            # Default paths
            "templates_dir": Path(__file__).parent.parent / "templates",
            "solution_dir": Path("solution"),
        }

        # Validate necessary configuration
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate required configuration settings.

        Raises:
            ValueError: If required configuration values are missing.
        """
        if not self.config.get("api_key"):
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
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
