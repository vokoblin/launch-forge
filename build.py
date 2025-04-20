#!/usr/bin/env python3
"""
Build script for LaunchForge application.
Creates executables for Windows, macOS, and Linux.
Uses a template-based approach with a direct .spec file template.
"""

import os
import sys
import shutil
import platform
import subprocess
import re

from src.models.constants import APP_VERSION


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


def generate_spec_file(output_name: str):
    """Create a spec file from template"""
    print(f"Creating spec file from template...")

    main_file = find_main_file()
    path_sep = get_path_separator()

    # Generate a temporary basic spec file to extract data paths
    temp_spec_name = f"temp_{output_name}"
    cmd = [
        "pyi-makespec",
        "--name", temp_spec_name,
        "--onefile",
        "--windowed",
        "--add-data", f"templates/bin{path_sep}templates",
        "--add-data", f"resources{path_sep}resources",
        "--icon", "resources/icons/app_icon.png",
        main_file
    ]
    run_command(cmd)

    # Read the generated spec file to extract necessary info
    temp_spec_path = f"{temp_spec_name}.spec"
    with open(temp_spec_path, "r") as f:
        orig_spec = f.read()

    # Extract the datas paths using regex
    datas_match = re.search(r'datas=\[(.*?)]', orig_spec, re.DOTALL)
    datas_content = datas_match.group(1)

    # Extract the icon path using regex
    icon_match = re.search(r"icon=\[(.*?)]", orig_spec, re.DOTALL)
    icon_content = icon_match.group(1)

    # Delete the temporary spec file
    os.remove(temp_spec_path)

    # Read the template
    with open("templates/launch_forge_spec_template.spec", "r") as f:
        template_content = f.read()

    # Replace placeholders
    spec_content = template_content.replace("{main_file}", main_file)
    spec_content = spec_content.replace("{output_name}", output_name)
    spec_content = spec_content.replace("{datas}", datas_content)
    spec_content = spec_content.replace("{icon_path}", icon_content.strip("'"))

    # Write the new spec file
    spec_path = f"{output_name}.spec"
    with open(spec_path, "w") as f:
        f.write(spec_content)

    print(f"Created spec file from template: {spec_path}")
    return spec_path


def build_for_platform(target_platform: str):
    """Build executable for given platform"""
    print(f"\n=== Building for {target_platform} ===\n")

    # Check if running on target platform
    current_platform = platform.system()
    if current_platform != target_platform and not (current_platform == "Darwin" and target_platform == "Macos"):
        print(f"Warning: Building {target_platform} executable on non-{target_platform} platform")

    output_name = f"LaunchForge-{target_platform}-v{APP_VERSION}"

    # Create customized spec file from template
    spec_file = generate_spec_file(output_name)

    # Build using the spec file
    cmd = ["pyinstaller", "--clean", spec_file]

    try:
        run_command(cmd)

        output_path = f"dist/{output_name}"

        # Define expected output paths based on platform
        if target_platform == "Windows":
            exe_output_path = f"{output_path}.exe"
            # If .exe doesn't exist but base does, rename it
            if not os.path.exists(exe_output_path) and os.path.exists(output_path):
                os.rename(output_path, exe_output_path)
                print(f"Renamed {output_path} to {exe_output_path}")
                output_path = exe_output_path
            else:
                output_path = exe_output_path

        if os.path.exists(output_path):
            if platform.system() != "Windows":
                os.chmod(output_path, 0o755)
            print(f"{target_platform} executable created: {output_path}")
        else:
            print(f"Warning: Expected output file not found: {output_path}")
            return False
    except Exception as e:
        print(f"Error building {target_platform} executable: {e}")
        return False

    return True


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

    # Remove spec files
    spec_files = [
        f"LaunchForge-Windows-v{APP_VERSION}.spec",
        f"LaunchForge-Linux-v{APP_VERSION}.spec",
        f"LaunchForge-Macos-v{APP_VERSION}.spec"
    ]

    for spec_file in spec_files:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"Removed {spec_file}")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Build for specified platforms
        platforms = sys.argv[1:]
        success = True

        for p in platforms:
            if p.lower() in ["windows", "linux", "macos"]:
                if not build_for_platform(p.capitalize()):
                    success = False
            else:
                print(f"Unknown platform: {p}")
                continue  # Skip unknown platforms but continue with others

            # Clean up build directories and temporary files after each build
            clean_build_files()

        if not success:
            return 1
    else:
        # If no platform specified, build for current platform
        current_platform = platform.system()
        if current_platform in ["Windows", "Linux", "Darwin"]:
            if not build_for_platform(current_platform.replace('Darwin', 'Macos')):
                return 1
        else:
            print(f"Unsupported platform: {current_platform}")
            return 1

        # Clean up build directories and temporary files
        clean_build_files()

    print("\n=== Build Complete ===\n")
    print("Built executables are in the dist directory:")
    print(f"  - Windows: dist/LaunchForge-Windows-v{APP_VERSION}.exe")
    print(f"  - Linux:   dist/LaunchForge-Linux-v{APP_VERSION}")
    print(f"  - macOS:   dist/LaunchForge-Macos-v{APP_VERSION}")

    return 0


if __name__ == "__main__":
    sys.exit(main())