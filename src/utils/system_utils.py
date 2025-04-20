"""
System utility functions for platform-specific operations.
"""

import os
import sys
import subprocess
import platform
import logging
from typing import Tuple, Optional, List

logger = logging.getLogger(__name__)

def get_platform() -> str:
    """
    Get the current platform name.
    
    Returns:
        str: 'windows', 'macos', or 'linux'
    """
    system = platform.system().lower()
    
    if system.startswith('win'):
        return 'windows'
    elif system.startswith('dar'):
        return 'macos'
    elif system.startswith('lin'):
        return 'linux'
    else:
        return system

def is_pyinstaller_available() -> bool:
    """
    Check if PyInstaller is available.
    
    Returns:
        bool: True if PyInstaller is available
    """
    try:
        subprocess.run(
            ["pyinstaller", "--version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_python_version() -> Tuple[int, int, int]:
    """
    Get the current Python version.
    
    Returns:
        Tuple[int, int, int]: Major, minor, and micro version numbers
    """
    return sys.version_info.major, sys.version_info.minor, sys.version_info.micro

def get_executable_extension() -> str:
    """
    Get the appropriate executable extension for the current platform.
    
    Returns:
        str: Executable extension (e.g., '.exe' on Windows)
    """
    platform_name = get_platform()
    
    if platform_name == 'windows':
        return '.exe'
    elif platform_name == 'macos':
        return '.app'
    else:  # Linux and others
        return ''

def open_file_explorer(path: str) -> bool:
    """
    Open the system file explorer at the specified path.
    
    Args:
        path: Directory path to open
        
    Returns:
        bool: True if successful
    """
    try:
        if get_platform() == 'windows':
            os.startfile(path)
        elif get_platform() == 'macos':
            subprocess.run(['open', path], check=True)
        else:  # Linux and others
            subprocess.run(['xdg-open', path], check=True)
        return True
    except Exception as e:
        logger.error(f"Failed to open file explorer at {path}: {e}")
        return False

def open_url(url: str) -> bool:
    """
    Open a URL in the default web browser.
    
    Args:
        url: URL to open
        
    Returns:
        bool: True if successful
    """
    try:
        if get_platform() == 'windows':
            os.startfile(url)
        elif get_platform() == 'macos':
            subprocess.run(['open', url], check=True)
        else:  # Linux and others
            subprocess.run(['xdg-open', url], check=True)
        return True
    except Exception as e:
        logger.error(f"Failed to open URL {url}: {e}")
        return False

def launch_executable(path: str, args: Optional[List[str]] = None) -> bool:
    """
    Launch an executable file.
    
    Args:
        path: Path to the executable
        args: Optional list of command-line arguments
        
    Returns:
        bool: True if successful
    """
    if args is None:
        args = []
    
    try:
        if get_platform() == 'windows':
            if args:
                subprocess.Popen([path] + args)
            else:
                os.startfile(path)
        else:  # macOS and Linux
            subprocess.Popen([path] + args)
        return True
    except Exception as e:
        logger.error(f"Failed to launch executable {path}: {e}")
        return False

def get_temp_directory() -> str:
    """
    Get the system temporary directory.
    
    Returns:
        str: Path to the temp directory
    """
    import tempfile
    return tempfile.gettempdir()

def is_admin() -> bool:
    """
    Check if the current process has administrator/root privileges.
    
    Returns:
        bool: True if running with elevated privileges
    """
    try:
        if get_platform() == 'windows':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:  # macOS and Linux
            return os.geteuid() == 0
    except Exception:
        return False

def get_platform_encoding() -> str:
    """
    Get the default encoding for the current platform.
    
    Returns:
        str: Default encoding (e.g., 'utf-8')
    """
    return sys.getfilesystemencoding() or 'utf-8'
