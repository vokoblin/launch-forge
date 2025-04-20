#!/usr/bin/env python3
"""
LaunchForge main application entry point.
"""

import sys
import os
import logging
import argparse
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.main_window import MainWindow
from src.models.constants import APP_NAME, APP_VERSION, CONFIG_DIR_PATH, ICON_DIR_PATH
from src.ui.styles import setup_styles, setup_dark_theme

# Configure logging
def setup_logging():
    """Set up logging configuration."""
    log_dir = os.path.join(CONFIG_DIR_PATH, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "main.log")

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(name)s][%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")

    return logger

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=f"{APP_NAME} v{APP_VERSION}")

    parser.add_argument(
        "--config",
        help="Path to configuration file to load"
    )

    parser.add_argument(
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Application theme (light or dark)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    return parser.parse_args()

def main():
    """Main application entry point."""
    # Set up logging
    logger = setup_logging()

    # Parse arguments
    args = parse_arguments()

    # Set log level based on debug flag
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    # Set application icon if available
    if os.path.exists(os.path.join(ICON_DIR_PATH, "app_icon.png")):
        app.setWindowIcon(QIcon(os.path.join(ICON_DIR_PATH, "app_icon.png")))

    # Apply theme
    if args.theme == "dark":
        setup_dark_theme()
    else:
        setup_styles()

    # Create main window (which now includes the splash screen)
    window = MainWindow()
    window.show()

    # Load configuration if specified
    if args.config:
        logger.info(f"Loading configuration from {args.config}")
        if os.path.exists(args.config):
            window.config_manager.load(args.config)
        else:
            logger.error(f"Configuration file not found: {args.config}")
            QMessageBox.warning(
                window,
                "Configuration Not Found",
                f"The specified configuration file was not found: {args.config}"
            )

    # Start the application event loop
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())