"""
Builder engine for creating launcher executables.
"""

import os
import logging
from typing import Callable, Optional, Tuple

from src.models.config_model import LauncherConfig
from src.models.constants import APP_NAME, APP_VERSION
from src.utils.system_utils import get_resource_path
from src.utils.embedding_utils import embed_config, verify_embedding

logger = logging.getLogger(__name__)

class BuilderEngine:
    """Handles the process of building launcher executables."""

    def __init__(self, config: LauncherConfig):
        """
        Initialize the builder engine.

        Args:
            config: The launcher configuration to use
        """
        self.config = config
        self.progress_callback = None

    def set_progress_callback(self, callback: Callable[[str, int], None]) -> None:
        """
        Set a callback function for reporting progress.

        Args:
            callback: Function that takes a message string and progress percentage
        """
        self.progress_callback = callback

    def report_progress(self, message: str, progress: int) -> None:
        """
        Report progress using the callback if set.

        Args:
            message: Progress message
            progress: Progress percentage (0-100)
        """
        if self.progress_callback:
            self.progress_callback(message, progress)
        logger.info(f"Build progress ({progress}%): {message}")

    def build(self, output_path: str) -> Tuple[bool, str]:
        """
        Build the launcher executable.

        Args:
            output_path: Path where the executable should be saved

        Returns:
            Tuple containing:
            - bool: True if build was successful
            - str: Error message if build failed, otherwise empty string
        """
        try:
            self.report_progress("Preparing to create launcher...", 10)

            # Ensure the configuration is valid
            self.config.target_os = self.config.target_os.lower()
            if self.config.target_os not in ['windows', 'macos', 'linux']:
                return False, f"Invalid target OS: {self.config.target_os}"

            # Get the appropriate template
            template_path = self._get_template_path(self.config.target_os)
            if not template_path:
                return False, f"No template found for OS: {self.config.target_os}"

            self.report_progress(f"Using template for {self.config.target_os}", 30)
            logger.info(f"Using template: {template_path}")

            # Prepare the configuration data
            config_data = self.config.to_dict()

            # Add metadata about LaunchForge
            config_data["created_with"] = f"{APP_NAME} v{APP_VERSION}"

            # Embed configuration in the template
            self.report_progress("Embedding configuration in launcher...", 60)
            success, error = embed_config(template_path, output_path, config_data)

            if not success:
                return False, error

            # Verify the embedding was successful
            self.report_progress("Verifying launcher...", 80)
            if not verify_embedding(output_path, config_data):
                return False, "Failed to verify configuration embedding"

            self.report_progress("Launcher created successfully", 100)
            return True, ""

        except Exception as e:
            logger.exception("Launcher creation failed with exception")
            return False, str(e)

    def _get_template_path(self, target_os: str) -> Optional[str]:
        """
        Get the path to the appropriate template executable.

        Args:
            target_os: Target operating system (windows, macos, linux)

        Returns:
            str: Path to the template executable, or None if not found
        """
        # Define template filenames for each OS
        template_filenames = {
            'windows': 'launcher_template_windows.exe',
            'macos': 'launcher_template_macos',
            'linux': 'launcher_template_linux'
        }

        template_filename = template_filenames.get(target_os.lower())
        if not template_filename:
            logger.error(f"No template filename defined for OS: {target_os}")
            return None

        template_path = get_resource_path(os.path.join('templates', template_filename))

        # Check if the template exists
        if not os.path.exists(template_path):
            logger.error(f"Template file not found: {template_path}")
            return None

        return template_path