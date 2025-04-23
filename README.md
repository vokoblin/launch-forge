# LaunchForge

A desktop application for creating custom game launchers and mod installers without any programming knowledge.

![LaunchForge](resources/icons/app_icon.png)

## Overview

LaunchForge is an all-in-one solution for game modders who want to distribute their mods with a simple, user-friendly launcher. The application allows you to:

1. Configure a custom game launcher with your branding and settings
2. Build standalone executable launchers for Windows, macOS, and Linux
3. Distribute a single file that handles downloading, installing, and launching your modded game

## Features

- **No Programming Required**: Simple user interface for all configuration
- **Direct URL Support**: Use direct download links from Google Drive, Dropbox, etc.
- **Game Directory Validation**: Ensure mods are installed to the correct folder
- **Auto-Detection**: Automatically find common game installation paths
- **Update Mechanism**: Install or update mods with a single click
- **Cross-Platform**: Create launchers for Windows, macOS, and Linux

## How It Works

### For Mod Creators

1. Download and run LaunchForge
2. Configure basic settings (name, description, game executable path)
3. Add mods with their download URLs and target paths
4. Configure validation files to identify the correct game folder
5. Build a standalone launcher executable
6. Share the launcher with your users

### For End Users

1. Download the launcher executable from the mod creator
2. Run the launcher
3. Select game directory (or it's auto-detected)
4. Click "Update/Install Mods" to download and install the mods
5. Click "Play Game" to launch the modded game

## Installation

### Requirements

- Python 3.6 or higher
- PyQt5
- PyInstaller

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/launch-forge.git
   cd launch-forge
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

### Pre-built Binaries

Pre-built executables are available for Windows, macOS, and Linux in the [Releases](https://github.com/vokoblin/launch-forge/releases) section.

## Building From Source

### Using Local Build Script

LaunchForge includes a build script that can create executables for Windows, Linux, and macOS:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   # Build for current platform only
   python build.py
   
   # Or specify platforms
   python build.py windows linux macos
   ```

3. Find the built executables in the `dist` directory:
   - `dist/LaunchForge-Windows.zip`
   - `dist/LaunchForge-Linux.zip`
   - `dist/LaunchForge-MacOS.zip`

### Using GitHub Actions

If you fork this repository, you can use GitHub Actions to automatically build executables:

1. Create a new release with a tag (e.g., `v1.0.0`)
2. GitHub Actions will automatically build executables for all platforms
3. Executables will be attached to the GitHub Release

## Usage Guide

### Creating a Game Launcher

1. **Basic Settings Tab**
   - Set the launcher name and description
   - Specify the game executable path (e.g., `game.exe` or `bin/game.exe`)
   - Set the version number

2. **Mods Tab**
   - Add each mod with a name, target path, and download URL
   - Target path is relative to the game folder (e.g., `mods/` or `data/textures/`)
   - Download URL must be a direct link to a ZIP file

3. **Advanced Settings Tab**
   - Select the target operating system
   - Configure validation files (used to identify the correct game folder)
   - Add default game locations for auto-detection

4. **Preview Tab**
   - See a preview of how your launcher will look
   - Review the functionality that will be included

5. **Build Tab**
   - Select an output path for the executable
   - Click "Build Launcher" to create the standalone launcher
   - Share the generated executable with your users

### Command Line Arguments

The application supports the following command-line arguments:

- `--config PATH`: Load a specific configuration file at startup
- `--theme THEME`: Use a specific theme (light or dark)
- `--debug`: Enable debug mode with verbose logging

Example:
```bash
python main.py --config my_config.json --theme dark
```

## Project Structure

```
launch-forge/
├── .github/workflows/          # GitHub Actions workflows
├── resources/                  # Application resources
│   └── icons/                  # UI icons
├── src/                        # Source code
│   ├── builder/                # Builder logic
│   ├── models/                 # Data models
│   ├── utils/                  # Utility functions
│   └── ui/                     # User interface
├── templates/                  # Template files
│   └── bin/                    # Pre-built launcher template files
├── build.py                    # Local build script
└── requirements.txt            # Project dependencies
```

## Troubleshooting

### Common Issues

1. **Download URLs not working**
   - Ensure you're using direct download links, not sharing links
   - For Google Drive, use a direct download URL generator

2. **Game not found**
   - Make sure your validation files correctly identify the game folder
   - Try adding more specific validation files

3. **Build errors**
   - Ensure PyInstaller is installed correctly
   - Check that you have all required dependencies installed
   - On Linux, you may need additional packages like `libxcb-xinerama0`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Uses [PyInstaller](https://www.pyinstaller.org/) for creating standalone executables