"""Unit tests for config.py module.

Tests for the ConfigurationManager class.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from provet.utils.config import ConfigurationManager


class TestConfigurationManager:
    """Test class for the ConfigurationManager."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"})
    @patch("provet.utils.config.load_dotenv")
    def test_init_with_env_vars(self, mock_load_dotenv):
        """Test initialization with environment variables.

        Given: Environment variables set
        When: A ConfigurationManager instance is created
        Then: It should load settings from environment variables.
        """
        # Execute
        config_manager = ConfigurationManager()

        # Assert
        assert config_manager.get("api_key") == "test-api-key"
        assert mock_load_dotenv.called

    @patch.dict(
        os.environ,
        {
            "OPENAI_API_KEY": "test-api-key",
            "OPENAI_MODEL": "custom-model",
            "TEMPERATURE": "0.5",
            "MAX_TOKENS": "1000",
            "CUSTOM_SYSTEM_INSTRUCTION": "Custom instruction",
        },
    )
    def test_init_with_custom_env_vars(self):
        """Test initialization with custom environment variables.

        Given: Custom environment variables set
        When: A ConfigurationManager instance is created
        Then: It should load the custom settings.
        """
        # Execute
        config_manager = ConfigurationManager()

        # Assert
        assert config_manager.get("api_key") == "test-api-key"
        assert config_manager.get("model") == "custom-model"
        assert config_manager.get("temperature") == 0.5
        assert config_manager.get("max_tokens") == 1000
        assert config_manager.get("custom_instruction") == "Custom instruction"

    @patch.dict(os.environ, {}, clear=True)  # Clear all environment variables
    @patch("provet.utils.config.load_dotenv")
    def test_init_without_api_key(self, mock_load_dotenv):
        """Test initialization without an API key.

        Given: No OPENAI_API_KEY environment variable
        When: A ConfigurationManager instance is created
        Then: It should raise a ValueError.
        """
        # Mock load_dotenv to ensure it doesn't load real .env
        mock_load_dotenv.return_value = False

        # Execute and Assert
        with pytest.raises(ValueError) as excinfo:
            ConfigurationManager()

        assert "OPENAI_API_KEY environment variable is not set" in str(excinfo.value)

    @patch.dict(
        os.environ, {"OPENAI_API_KEY": "test-api-key", "OPENAI_MODEL": "gpt-4.1-nano"}
    )
    def test_get_existing_key(self):
        """Test getting an existing configuration key.

        Given: A ConfigurationManager with initialized settings
        When: get is called with an existing key
        Then: It should return the value for that key.
        """
        # Setup
        config_manager = ConfigurationManager()

        # Execute and Assert
        assert config_manager.get("api_key") == "test-api-key"
        assert (
            config_manager.get("model") == "gpt-4.1-nano"
        )  # Updated to match actual model

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"})
    def test_get_nonexistent_key(self):
        """Test getting a non-existent configuration key.

        Given: A ConfigurationManager
        When: get is called with a non-existent key
        Then: It should return the default value.
        """
        # Setup
        config_manager = ConfigurationManager()

        # Execute and Assert
        assert config_manager.get("nonexistent_key") is None
        assert config_manager.get("nonexistent_key", "default") == "default"

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"})
    def test_set(self):
        """Test setting a configuration value.

        Given: A ConfigurationManager
        When: set is called with a key and value
        Then: It should update the configuration with the new value.
        """
        # Setup
        config_manager = ConfigurationManager()

        # Execute
        config_manager.set("new_key", "new_value")

        # Assert
        assert config_manager.get("new_key") == "new_value"

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"})
    def test_update(self):
        """Test updating multiple configuration values.

        Given: A ConfigurationManager
        When: update is called with a dictionary of new values
        Then: It should update the configuration with all the new values.
        """
        # Setup
        config_manager = ConfigurationManager()
        new_config = {
            "model": "gpt-4-turbo",
            "temperature": 0.8,
            "new_key": "new_value",
        }

        # Execute
        config_manager.update(new_config)

        # Assert
        assert config_manager.get("model") == "gpt-4-turbo"
        assert config_manager.get("temperature") == 0.8
        assert config_manager.get("new_key") == "new_value"
        # Original values should remain unchanged
        assert config_manager.get("api_key") == "test-api-key"

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"})
    def test_default_paths(self):
        """Test default paths in configuration.

        Given: A ConfigurationManager with no path overrides
        When: The configuration is accessed
        Then: It should have valid default paths.
        """
        # Execute
        config_manager = ConfigurationManager()

        # Assert
        templates_dir = config_manager.get("templates_dir")
        solution_dir = config_manager.get("solution_dir")

        assert isinstance(templates_dir, Path)
        assert isinstance(solution_dir, Path)
        assert templates_dir.name == "templates"
        assert solution_dir.name == "solution"
