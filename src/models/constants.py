"""
Constants and default values for the application.
"""

from typing import Dict, List
import os
from pathlib import Path

# Application information
APP_NAME = "LaunchForge"
APP_VERSION = "0.0.1"
APP_AUTHOR = "Vokoblin"

# Default values for new configurations
DEFAULT_CONFIG_NAME = "My Game Mod Launcher"
DEFAULT_CONFIG_DESCRIPTION = "Install awesome mods for your game!"
DEFAULT_GAME_EXE = "game.exe"
DEFAULT_VERSION = "1.0.0"
DEFAULT_TARGET_OS = "windows"

# Default first mod
DEFAULT_MOD_NAME = "Base Mod"
DEFAULT_MOD_TARGET_PATH = "mods/"
DEFAULT_MOD_DOWNLOAD_URL = ""
DEFAULT_MOD_DESCRIPTION = "The core mod files"

# Common game location patterns by platform
DEFAULT_GAME_LOCATIONS: Dict[str, List[str]] = {
    "windows": [
        "C:/Program Files (x86)/Steam/steamapps/common",
        "C:/Program Files/Steam/steamapps/common",
        "C:/Games",
        "D:/Games",
        "C:/Program Files (x86)/Epic Games",
        "C:/Program Files/Epic Games"
    ],
    "macos": [
        "~/Library/Application Support/Steam/steamapps/common",
        "~/Games"
    ],
    "linux": [
        "~/.steam/steam/steamapps/common",
        "~/Games"
    ]
}

# File extensions for each platform
EXECUTABLE_EXTENSIONS: Dict[str, str] = {
    "windows": ".exe",
    "macos": ".app",
    "linux": ""  # No extension on Linux
}

# Template file paths
def get_template_path() -> str:
    """Get the path to template files based on execution context."""
    # Check for development environment
    if os.path.exists(os.path.join(os.path.dirname(__file__), "../../templates")):
        return os.path.join(os.path.dirname(__file__), "../../templates")
    
    # When running as a package
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates")

LAUNCHER_TEMPLATE_PATH = os.path.join(get_template_path(), "launcher_template.py")

# Config storage paths
def get_config_dir() -> str:
    """Get the path to user config directory."""
    home = Path.home()
    config_dir_name = APP_NAME.lower().replace(' ', '-')
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(home, "AppData", "Local", config_dir_name)
    elif os.name == 'posix':  # macOS and Linux
        config_dir = os.path.join(home, "." + config_dir_name)
    else:
        config_dir = os.path.join(home, "." + config_dir_name)
    # Ensure directory exists
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

CONFIG_DIR_PATH = get_config_dir()
CONFIG_PATH = os.path.join(CONFIG_DIR_PATH, "config.json")

# Icons and resources
def get_resources_path() -> str:
    """Get the path to resources based on execution context."""
    # Check for development environment
    if os.path.exists(os.path.join(os.path.dirname(__file__), "../../resources")):
        return os.path.join(os.path.dirname(__file__), "../../resources")
    
    # When running as a package
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "../resources")

RESOURCES_DIR_PATH = get_resources_path()
ICON_DIR_PATH = os.path.join(RESOURCES_DIR_PATH, "icons")

# UI Constants
UI_PADDING = 10
UI_SPACING = 5
UI_MIN_WIDTH = 900
UI_MIN_HEIGHT = 600

# Status Messages
MSG_CONFIG_SAVED = "Configuration saved successfully"
MSG_CONFIG_LOADED = "Configuration loaded successfully"
MSG_BUILD_STARTED = "Building launcher..."
MSG_BUILD_COMPLETED = "Launcher built successfully!"
MSG_BUILD_FAILED = "Failed to build launcher"
