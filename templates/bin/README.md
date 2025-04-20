# Launcher Templates

This directory contains pre-built launcher templates for different operating systems:

- `launcher_template_windows.exe`: Template for Windows
- `launcher_template_macos`: Template for macOS
- `launcher_template_linux`: Template for Linux

These templates are automatically built by GitHub Actions when the launcher template code is modified. They serve as the base executables for creating custom game mod launchers.

## How Templates Are Used

When a user creates a launcher through LaunchForge, the system:

1. Selects the appropriate template for their target OS
2. Embeds their configuration data in the executable
3. Creates a custom-branded launcher with all their settings

## Manual Building

If you need to build these templates manually, use:

```bash
# Run from the project root
python -m PyInstaller --clean --onefile --windowed --icon=resources/icons/app_icon.png --name=launcher_template_windows templates/launcher_template.py
```

After building, move the resulting executable to this directory.
