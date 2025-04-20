"""
Validator for checking configuration validity.
"""

import logging
from typing import Dict, List
import re
import os

from src.models.config_model import LauncherConfig

logger = logging.getLogger(__name__)

def validate_config(config: LauncherConfig) -> Dict[str, str]:
    """
    Validate a launcher configuration.
    
    Args:
        config: Configuration to validate
        
    Returns:
        Dict[str, str]: Dictionary of field names and error messages,
                      empty if configuration is valid
    """
    errors = {}
    
    # Basic validation
    if not config.name.strip():
        errors["name"] = "Launcher name is required"
    
    if not config.game_exe.strip():
        errors["game_exe"] = "Game executable path is required"
    
    # Validate version format (optional)
    if config.version and not _is_valid_version(config.version):
        errors["version"] = "Version must be in format X.Y.Z (e.g., 1.0.0)"
    
    # Validate mods
    if not config.mods:
        errors["mods"] = "At least one mod is required"
    
    for i, mod in enumerate(config.mods):
        prefix = f"mod_{i}"
        
        if not mod.name.strip():
            errors[f"{prefix}_name"] = f"Mod {i+1} requires a name"
        
        if not mod.target_path.strip():
            errors[f"{prefix}_target_path"] = f"Mod '{mod.name}' requires a target path"
        
        if not mod.download_url.strip():
            errors[f"{prefix}_download_url"] = f"Mod '{mod.name}' requires a download URL"
        elif not _is_valid_url(mod.download_url):
            errors[f"{prefix}_download_url"] = f"Mod '{mod.name}' has an invalid download URL"
    
    # Validate validation files
    if not config.validation_files:
        errors["validation_files"] = "At least one validation file is required"
    
    # Validate target OS
    if config.target_os not in ["windows", "macos", "linux"]:
        errors["target_os"] = "Target OS must be 'windows', 'macos', or 'linux'"
    
    return errors

def _is_valid_version(version: str) -> bool:
    """
    Check if a version string is valid (e.g., "1.0.0").
    
    Args:
        version: Version string to check
        
    Returns:
        bool: True if valid
    """
    version_pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(version_pattern, version))

def _is_valid_url(url: str) -> bool:
    """
    Check if a URL is valid.
    
    Args:
        url: URL to check
        
    Returns:
        bool: True if valid
    """
    # Basic URL validation
    url_pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    if not re.match(url_pattern, url):
        # Check for Google Drive and Dropbox URLs
        gdrive_pattern = r'^https://drive\.google\.com/\S+$'
        dropbox_pattern = r'^https://www\.dropbox\.com/\S+$'
        
        if not (re.match(gdrive_pattern, url) or re.match(dropbox_pattern, url)):
            return False
    
    return True

def validate_path_for_os(path: str, target_os: str) -> bool:
    """
    Validate that a path is appropriate for the target OS.
    
    Args:
        path: Path to validate
        target_os: Target OS (windows, macos, linux)
        
    Returns:
        bool: True if valid
    """
    if target_os == "windows":
        # Windows paths can't contain: <>:"/\|?*
        invalid_chars = r'[<>:"/\\|?*]'
        return not bool(re.search(invalid_chars, path))
    else:
        # macOS and Linux paths can't contain null bytes
        return '\0' not in path

def validate_file_exists(path: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        path: Path to the file
        
    Returns:
        bool: True if the file exists
    """
    return os.path.isfile(path)

def validate_directory_exists(path: str) -> bool:
    """
    Check if a directory exists.
    
    Args:
        path: Path to the directory
        
    Returns:
        bool: True if the directory exists
    """
    return os.path.isdir(path)

def validate_game_directory(directory: str, validation_files: List[str]) -> bool:
    """
    Validate that a directory contains the specified validation files.
    
    Args:
        directory: Path to the directory
        validation_files: List of files that should exist
        
    Returns:
        bool: True if all validation files exist
    """
    for file_path in validation_files:
        full_path = os.path.join(directory, file_path)
        if not os.path.exists(full_path):
            return False
    return True

def get_validation_errors_text(errors: Dict[str, str]) -> str:
    """
    Convert validation errors to human-readable text.
    
    Args:
        errors: Dictionary of field names and error messages
        
    Returns:
        str: Human-readable error text
    """
    if not errors:
        return "No validation errors."
    
    error_text = "The following validation errors were found:\n\n"
    for field, message in errors.items():
        error_text += f"• {message}\n"
    
    return error_text
