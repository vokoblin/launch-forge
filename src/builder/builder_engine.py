"""
Builder engine for creating launcher executables.
"""

import os
import json
import shutil
import tempfile
import logging
import subprocess
from typing import Callable, Optional, Tuple

from src.models.config_model import LauncherConfig
from src.models.constants import LAUNCHER_TEMPLATE_PATH, EXECUTABLE_EXTENSIONS

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
        self.template_path = LAUNCHER_TEMPLATE_PATH
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
            self.report_progress("Preparing build environment...", 5)

            # Create a temporary directory for the build
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create launcher script with embedded config
                self.report_progress("Creating launcher script and config...", 15)
                script_path = self._create_launcher_script(temp_dir)

                if not script_path:
                    return False, "Failed to create launcher script"

                # Build the executable
                self.report_progress("Building executable...", 30)
                success, error = self._build_executable(script_path, output_path)

                if not success:
                    return False, f"Failed to build executable: {error}"

                self.report_progress("Finalizing build...", 95)

            self.report_progress("Build completed successfully", 100)
            return True, ""

        except Exception as e:
            logger.exception("Build failed with exception")
            return False, str(e)

    def _create_launcher_script(self, temp_dir: str) -> Optional[str]:
        """
        Create the launcher script and configuration file.

        Args:
            temp_dir: Temporary directory for build files

        Returns:
            str: Path to the created script, or None if creation failed
        """
        try:
            # Read the template
            with open(self.template_path, 'r') as f:
                template = f.read()

            # Write the configuration to a JSON file
            config_path = os.path.join(temp_dir, "launcher_config.json")
            with open(config_path, 'w') as f:
                json.dump(self.config.to_dict(), f, indent=4)

            # Write the script
            script_path = os.path.join(temp_dir, "launcher.py")
            with open(script_path, 'w') as f:
                f.write(template)

            logger.info(f"Created launcher script: {script_path}")
            logger.info(f"Created configuration file: {config_path}")
            return script_path

        except Exception as e:
            logger.error(f"Failed to create launcher script: {e}")
            return None

    def _build_executable(self, script_path: str, output_path: str) -> Tuple[bool, str]:
        """
        Build the executable using PyInstaller.

        Args:
            script_path: Path to the Python script to compile
            output_path: Path where the executable should be saved

        Returns:
            Tuple containing:
            - bool: True if build was successful
            - str: Error message if build failed, otherwise empty string
        """
        try:
            # Create safe name from config name (alphanumeric only)
            safe_name = ''.join(c if c.isalnum() else '_' for c in self.config.name)

            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Get path to config file
            config_file = os.path.join(os.path.dirname(script_path), "launcher_config.json")

            # Platform-specific path separator for PyInstaller
            path_sep = ';' if os.name == 'nt' else ':'

            # Define PyInstaller command with added data file
            pyinstaller_args = [
                'pyinstaller',
                '--onefile',
                '--windowed',
                f'--name={safe_name}',
                '--clean',
                f'--add-data={config_file}{path_sep}.',  # Add config file as a resource
                script_path
            ]

            # Add icon if available
            # icon_path = os.path.join(os.path.dirname(__file__), '../../resources/icons/app_icon.ico')
            # if os.path.exists(icon_path):
            #     pyinstaller_args.extend(['--icon', icon_path])

            # Run PyInstaller
            self.report_progress("Running PyInstaller...", 40)
            process = subprocess.Popen(
                pyinstaller_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Monitor PyInstaller progress
            progress = 40
            for line in iter(process.stdout.readline, ''):
                if progress < 80:
                    progress += 1
                    self.report_progress(f"Building executable: {line.strip()}", progress)

            # Wait for process to complete
            process.wait()

            if process.returncode != 0:
                # Capture error output
                error_output = process.stderr.read()
                return False, f"PyInstaller failed with code {process.returncode}: {error_output}"

            # Move the executable to the requested location
            ext = EXECUTABLE_EXTENSIONS.get(self.config.target_os, "")
            dist_path = os.path.join('dist', f"{safe_name}{ext}")

            if not os.path.exists(dist_path):
                return False, f"PyInstaller did not create the expected file at {dist_path}"

            self.report_progress("Copying executable to destination...", 85)
            shutil.copy2(dist_path, output_path)

            # Copy the config file to the same directory as the executable
            # This allows users to modify the configuration without rebuilding
            config_output_path = os.path.join(os.path.dirname(output_path), "launcher_config.json")
            shutil.copy2(config_file, config_output_path)
            logger.info(f"Config file copied to: {config_output_path}")

            # Clean up PyInstaller output
            self.report_progress("Cleaning up...", 90)
            if os.path.exists('dist'):
                shutil.rmtree('dist')
            if os.path.exists('build'):
                shutil.rmtree('build')
            spec_file = f"{safe_name}.spec"
            if os.path.exists(spec_file):
                os.remove(spec_file)

            return True, ""

        except Exception as e:
            logger.exception("PyInstaller build failed")
            return False, str(e)