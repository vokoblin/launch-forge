"""
Configuration manager for handling configuration loading, saving and validation.
"""

import os
import json
import logging
from typing import Optional, Dict
from datetime import datetime

from src.builder.validator import validate_config
from src.models.config_model import LauncherConfig, ModConfig
from src.models.constants import (
    CONFIG_PATH, DEFAULT_CONFIG_NAME, DEFAULT_CONFIG_DESCRIPTION,
    DEFAULT_GAME_EXE, DEFAULT_VERSION, DEFAULT_TARGET_OS,
    DEFAULT_MOD_NAME, DEFAULT_MOD_TARGET_PATH, DEFAULT_MOD_DOWNLOAD_URL,
    DEFAULT_MOD_DESCRIPTION
)

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages the launcher configuration data."""

    def __init__(self):
        """Initialize the configuration manager."""
        self.config = self._create_default_config()
        self.config_path = CONFIG_PATH

    def _create_default_config(self) -> LauncherConfig:
        """Create a default configuration."""
        default_mod = ModConfig(
            name=DEFAULT_MOD_NAME,
            target_path=DEFAULT_MOD_TARGET_PATH,
            download_url=DEFAULT_MOD_DOWNLOAD_URL,
            description=DEFAULT_MOD_DESCRIPTION,
            is_required=True
        )

        return LauncherConfig(
            name=DEFAULT_CONFIG_NAME,
            description=DEFAULT_CONFIG_DESCRIPTION,
            game_exe=DEFAULT_GAME_EXE,
            version=DEFAULT_VERSION,
            mods=[default_mod],
            validation_files=[DEFAULT_GAME_EXE],
            target_os=DEFAULT_TARGET_OS
        )

    def load(self, config_path: Optional[str] = None) -> bool:
        """
        Load configuration from a file.

        Args:
            config_path: Path to the configuration file (optional)

        Returns:
            bool: True if configuration was successfully loaded
        """
        path = config_path or self.config_path

        if not os.path.exists(path):
            logger.info(f"Configuration file not found at {path}")
            return False

        try:
            with open(path, 'r') as f:
                data = json.load(f)

            self.config = LauncherConfig.from_dict(data)
            logger.info(f"Configuration loaded from {path}")

            if config_path:  # If a specific path was provided, update the default
                self.config_path = config_path

            return True

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to load configuration: {e}")
            return False

    def save(self, config_path: Optional[str] = None) -> bool:
        """
        Save configuration to a file.

        Args:
            config_path: Path to save the configuration file (optional)

        Returns:
            bool: True if configuration was successfully saved
        """
        path = config_path or self.config_path

        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            # Update timestamp
            self.config.updated = datetime.now().isoformat()

            with open(path, 'w') as f:
                json.dump(self.config.to_dict(), f, indent=2)

            logger.info(f"Configuration saved to {path}")

            if config_path:  # If a specific path was provided, update the default
                self.config_path = config_path

            return True

        except (OSError, TypeError) as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    def export_config(self, export_path: str) -> bool:
        """
        Export the current configuration to a file.
        This is a specialized version to export for the builder.

        Args:
            export_path: Path to export the configuration

        Returns:
            bool: True if configuration was successfully exported
        """
        try:
            config_data = self.config.to_dict()

            with open(export_path, 'w') as f:
                json.dump(config_data, f, indent=2)

            logger.info(f"Configuration exported to {export_path}")
            return True

        except (OSError, TypeError) as e:
            logger.error(f"Failed to export configuration: {e}")
            return False

    def import_config(self, import_path: str) -> bool:
        """
        Import a configuration from a file.

        Args:
            import_path: Path to the configuration file to import

        Returns:
            bool: True if configuration was successfully imported
        """
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)

            self.config = LauncherConfig.from_dict(data)
            logger.info(f"Configuration imported from {import_path}")

            # Save to default location
            self.save()

            return True

        except (json.JSONDecodeError, KeyError, ValueError, OSError) as e:
            logger.error(f"Failed to import configuration: {e}")
            return False

    def validate(self) -> Dict[str, str]:
        """
        Validate the current configuration.

        Returns:
            Dict[str, str]: Dictionary of field names and error messages,
                           empty if configuration is valid
        """
        return validate_config(self.config)
