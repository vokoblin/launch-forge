#!/usr/bin/env python3
"""
Build script for LaunchForge application.
Creates executables for Windows, macOS, and Linux.
"""

import os
import sys
import shutil
import platform
import subprocess


def run_command(command, check=True):
    """Run a command and print output"""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, check=check, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    return result


def get_path_separator():
    """Return the correct path separator for PyInstaller based on current platform"""
    return ";" if platform.system() == "Windows" else ":"


def build_windows():
    """Build Windows executable"""
    print("\n=== Building for Windows ===\n")

    # Check if running on Windows
    if platform.system() != "Windows":
        print("Warning: Building Windows executable on non-Windows platform")

    # Create platform-specific build folder with proper Windows paths
    platform_dir = os.path.join("dist", "windows")
    os.makedirs(platform_dir, exist_ok=True)

    # Ensure resources directory exists
    os.makedirs("resources", exist_ok=True)

    # Build with PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name", "LaunchForge",
        "--distpath", platform_dir
    ]

    # Only add resources if directory is not empty
    if os.path.exists("resources") and os.listdir("resources"):
        cmd.extend(["--add-data", f"resources{get_path_separator()}resources"])

    cmd.append(find_main_file())

    # Check if icon exists
    if os.path.exists("resources/icons/app_icon.ico"):
        cmd.extend(["--icon", "resources/icons/app_icon.ico"])
    elif os.path.exists("resources/icons/app_icon.png"):
        print("Warning: No .ico file found, using .png")
        cmd.extend(["--icon", "resources/icons/app_icon.png"])

    try:
        run_command(cmd)
        print(f"Windows executable created: {platform_dir}/LaunchForge.exe")
    except Exception as e:
        print(f"Error building Windows executable: {e}")


def build_linux():
    """Build Linux executable"""
    print("\n=== Building for Linux ===\n")

    # Check if running on Linux
    if platform.system() != "Linux":
        print("Warning: Building Linux executable on non-Linux platform")

    # Create platform-specific build folder
    platform_dir = "dist/linux"
    os.makedirs(platform_dir, exist_ok=True)

    # Build with PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name", "LaunchForge",
        "--distpath", platform_dir,
        "--add-data", f"resources{get_path_separator()}resources",
        find_main_file()
    ]

    # Check if icon exists
    if os.path.exists("resources/icons/app_icon.png"):
        cmd.extend(["--icon", "resources/icons/app_icon.png"])

    run_command(cmd)

    # Make executable
    os.chmod(f"{platform_dir}/LaunchForge", 0o755)
    print(f"Linux executable created: {platform_dir}/LaunchForge")


def build_macos():
    """Build macOS executable"""
    print("\n=== Building for macOS ===\n")

    # Check if running on macOS
    if platform.system() != "Darwin":
        print("Warning: Building macOS executable on non-macOS platform")

    # Create platform-specific build folder
    platform_dir = "dist/macos"
    os.makedirs(platform_dir, exist_ok=True)

    # Build with PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name", "LaunchForge",
        "--distpath", platform_dir,
        "--add-data", f"resources{get_path_separator()}resources",
        find_main_file()
    ]

    # Check if icon exists
    if os.path.exists("resources/icons/app_icon.icns"):
        cmd.extend(["--icon", "resources/icons/app_icon.icns"])
    elif os.path.exists("resources/icons/app_icon.png"):
        print("Warning: No .icns file found, using .png")
        cmd.extend(["--icon", "resources/icons/app_icon.png"])

    run_command(cmd)

    # Make executable
    os.chmod(f"{platform_dir}/LaunchForge", 0o755)
    print(f"macOS executable created: {platform_dir}/LaunchForge")


def find_main_file():
    """Find the main Python file to build"""
    main_file = "src/main.py"

    if os.path.exists(main_file):
        print(f"Found main file: {main_file}")
        return main_file

    # If the file doesn't exist, raise an error
    print("ERROR: Could not find src/main.py!")
    sys.exit(1)  # Exit with error code


def clean_build_files():
    """Clean up build directory and other temporary files"""
    print("\nCleaning up build files...")

    # Remove build directory
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("Removed build directory")

    # Remove spec file
    spec_file = "LaunchForge.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"Removed {spec_file}")


def main():
    """Main function"""
    # Initial cleanup of old dist directory
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    # Create the dist directory
    os.makedirs("dist", exist_ok=True)

    # Detect platform and build for it
    current_platform = platform.system()

    if len(sys.argv) > 1:
        # Build for specified platforms
        platforms = sys.argv[1:]
        for p in platforms:
            if p.lower() == "windows":
                build_windows()
            elif p.lower() == "linux":
                build_linux()
            elif p.lower() == "macos":
                build_macos()
            else:
                print(f"Unknown platform: {p}")
                continue  # Skip unknown platforms but continue with others

            # Clean up build directories and temporary files after each build
            clean_build_files()
    else:
        # If no platform specified, build for current platform
        if current_platform == "Windows":
            build_windows()
        elif current_platform == "Linux":
            build_linux()
        elif current_platform == "Darwin":
            build_macos()
        else:
            print(f"Unsupported platform: {current_platform}")
            return 1

        # Clean up build directories and temporary files
        clean_build_files()

    print("\n=== Build Complete ===\n")
    print("Built executables are in platform-specific directories under dist/:")
    print("  - Windows: dist/windows/LaunchForge.exe")
    print("  - Linux:   dist/linux/LaunchForge")
    print("  - macOS:   dist/macos/LaunchForge")

    return 0


if __name__ == "__main__":
    sys.exit(main())