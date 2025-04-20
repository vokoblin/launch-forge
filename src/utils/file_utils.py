"""
File utility functions for the application.
"""

import os
import hashlib
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

def ensure_dir_exists(directory: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory
        
    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except OSError as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False

def file_exists(file_path: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if file exists
    """
    return os.path.isfile(file_path)

def directory_exists(directory: str) -> bool:
    """
    Check if a directory exists.
    
    Args:
        directory: Path to the directory
        
    Returns:
        bool: True if directory exists
    """
    return os.path.isdir(directory)

def calculate_file_hash(file_path: str) -> Optional[str]:
    """
    Calculate SHA-256 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: Hex digest of the hash, or None if file doesn't exist
    """
    if not file_exists(file_path):
        return None
    
    try:
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            # Read in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        logger.error(f"Failed to hash file {file_path}: {e}")
        return None

def find_files_by_extension(directory: str, extension: str) -> List[str]:
    """
    Find all files with a specific extension in a directory.
    
    Args:
        directory: Directory to search
        extension: File extension to look for (e.g., ".exe")
        
    Returns:
        List[str]: List of full file paths
    """
    if not directory_exists(directory):
        return []
    
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extension.lower()):
                found_files.append(os.path.join(root, file))
    
    return found_files

def get_relative_path(base_path: str, full_path: str) -> str:
    """
    Get the relative path from a base path.
    
    Args:
        base_path: Base directory path
        full_path: Full path to the file
        
    Returns:
        str: Relative path
    """
    try:
        return os.path.relpath(full_path, base_path)
    except ValueError:
        # Happens with paths on different drives in Windows
        return full_path

def get_basename(file_path: str) -> str:
    """
    Get the base name of a file path (filename without directory).
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: Base name
    """
    return os.path.basename(file_path)

def get_file_extension(file_path: str) -> str:
    """
    Get the extension of a file, including the dot.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: File extension (e.g., ".txt")
    """
    _, extension = os.path.splitext(file_path)
    return extension.lower()

def get_common_game_directories() -> List[str]:
    """
    Get a list of common game installation directories based on the platform.
    
    Returns:
        List[str]: List of common game directories
    """
    common_dirs = []
    
    # Windows-specific directories
    if os.name == 'nt':
        drives = ['C:', 'D:', 'E:', 'F:']
        
        for drive in drives:
            if os.path.exists(drive):
                # Steam
                steam_dirs = [
                    os.path.join(drive, "Program Files", "Steam", "steamapps", "common"),
                    os.path.join(drive, "Program Files (x86)", "Steam", "steamapps", "common"),
                    os.path.join(drive, "SteamLibrary", "steamapps", "common")
                ]
                
                # Epic Games
                epic_dirs = [
                    os.path.join(drive, "Program Files", "Epic Games"),
                    os.path.join(drive, "Program Files (x86)", "Epic Games")
                ]
                
                # Other common locations
                other_dirs = [
                    os.path.join(drive, "Games"),
                    os.path.join(drive, "Program Files", "Games"),
                    os.path.join(drive, "Program Files (x86)", "Games")
                ]
                
                for d in steam_dirs + epic_dirs + other_dirs:
                    if os.path.exists(d):
                        common_dirs.append(d)
    
    # macOS-specific directories
    elif os.name == 'posix' and os.path.exists('/Applications'):
        home = str(Path.home())
        common_dirs.extend([
            os.path.join(home, "Library", "Application Support", "Steam", "steamapps", "common"),
            "/Applications",
            os.path.join(home, "Games")
        ])
    
    # Linux-specific directories
    elif os.name == 'posix':
        home = str(Path.home())
        common_dirs.extend([
            os.path.join(home, ".steam", "steam", "steamapps", "common"),
            os.path.join(home, ".local", "share", "Steam", "steamapps", "common"),
            os.path.join(home, "Games")
        ])
    
    return [d for d in common_dirs if os.path.exists(d)]
