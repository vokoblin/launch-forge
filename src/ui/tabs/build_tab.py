"""
Build tab for building the launcher executable.
"""

import os
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QLineEdit, 
    QPushButton, QProgressBar, QHBoxLayout, QFileDialog, 
    QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal

from src.builder.config_manager import ConfigManager
from src.builder.builder_engine import BuilderEngine
from src.utils.system_utils import open_file_explorer, get_executable_extension
from src.models.constants import EXECUTABLE_EXTENSIONS

logger = logging.getLogger(__name__)

class BuildThread(QThread):
    """Thread for running the build process in the background."""
    
    progress_updated = pyqtSignal(str, int)
    build_completed = pyqtSignal(bool, str, str)
    
    def __init__(self, config_manager: ConfigManager, output_path: str):
        """
        Initialize the build thread.
        
        Args:
            config_manager: Configuration manager instance
            output_path: Path where the executable should be saved
        """
        super().__init__()
        self.config_manager = config_manager
        self.output_path = output_path
    
    def run(self):
        """Run the build process."""
        try:
            # Create builder engine
            builder = BuilderEngine(self.config_manager.config)
            builder.set_progress_callback(self.report_progress)
            
            # Build the launcher
            success, error = builder.build(self.output_path)
            
            # Emit result
            self.build_completed.emit(success, error, self.output_path)
            
        except Exception as e:
            logger.exception("Build thread failed")
            self.build_completed.emit(False, str(e), "")
    
    def report_progress(self, message: str, progress: int):
        """
        Report build progress.
        
        Args:
            message: Progress message
            progress: Progress percentage (0-100)
        """
        self.progress_updated.emit(message, progress)

class BuildTab(QWidget):
    """Tab for building the launcher executable."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the build tab.
        
        Args:
            config_manager: Configuration manager instance
        """
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title and description
        title_label = QLabel("Build Launcher")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        description_label = QLabel(
            "Build a standalone launcher executable that can be distributed to users. "
            "The launcher will contain all your configuration settings and will handle "
            "downloading and installing mods."
        )
        description_label.setWordWrap(True)
        layout.addWidget(description_label)
        
        # Output path group
        output_group = QGroupBox("Output Settings")
        output_layout = QHBoxLayout(output_group)
        
        self.output_path_input = QLineEdit()
        self.output_path_input.setPlaceholderText("Select output path for the executable")
        output_layout.addWidget(self.output_path_input)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_output_path)
        output_layout.addWidget(browse_button)
        
        layout.addWidget(output_group)
        
        # Build button
        build_button_layout = QHBoxLayout()
        build_button_layout.addStretch()
        
        self.build_button = QPushButton("Build Launcher")
        self.build_button.setMinimumHeight(50)
        self.build_button.setMinimumWidth(200)
        self.build_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px; }"
            "QPushButton:hover { background-color: #45A049; }"
            "QPushButton:pressed { background-color: #3D8B40; }"
            "QPushButton:disabled { background-color: #CCCCCC; color: #666666; }"
        )
        self.build_button.clicked.connect(self.start_build)
        build_button_layout.addWidget(self.build_button)
        
        build_button_layout.addStretch()
        layout.addLayout(build_button_layout)
        
        # Progress group
        self.progress_group = QGroupBox("Build Progress")
        self.progress_group.setVisible(False)
        progress_layout = QVBoxLayout(self.progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("Preparing build...")
        progress_layout.addWidget(self.progress_label)
        
        layout.addWidget(self.progress_group)
        
        # Results group
        self.results_group = QGroupBox("Build Results")
        self.results_group.setVisible(False)
        results_layout = QVBoxLayout(self.results_group)
        
        self.results_label = QLabel()
        self.results_label.setWordWrap(True)
        results_layout.addWidget(self.results_label)
        
        results_buttons_layout = QHBoxLayout()
        
        self.open_folder_button = QPushButton("Open Containing Folder")
        self.open_folder_button.clicked.connect(self.open_output_folder)
        results_buttons_layout.addWidget(self.open_folder_button)
        
        self.new_build_button = QPushButton("Start New Build")
        self.new_build_button.clicked.connect(self.reset_build_ui)
        results_buttons_layout.addWidget(self.new_build_button)
        
        results_layout.addLayout(results_buttons_layout)
        layout.addWidget(self.results_group)
        
        # Add spacer to push everything to the top
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Help text
        help_group = QGroupBox("Help")
        help_layout = QVBoxLayout(help_group)
        
        help_text = (
            "<b>Building Process:</b><br>"
            "1. The builder will create a standalone executable containing your configuration.<br>"
            "2. The executable will handle downloading and installing mods when users run it.<br>"
            "3. The build process may take several minutes to complete.<br><br>"
            "<b>Requirements:</b><br>"
            "• PyInstaller must be installed on your system.<br>"
            "• Internet connection is required for the build process.<br>"
            "• The generated executable will work on the same operating system it was built on."
        )
        
        help_label = QLabel(help_text)
        help_label.setTextFormat(Qt.RichText)
        help_label.setWordWrap(True)
        help_layout.addWidget(help_label)
        
        layout.addWidget(help_group)
    
    def set_config_manager(self, config_manager: ConfigManager):
        """
        Set a new configuration manager.
        
        Args:
            config_manager: New configuration manager instance
        """
        self.config_manager = config_manager
    
    def refresh(self):
        """Refresh the UI with current configuration data."""
        # Set a default output path based on the configuration name
        safe_name = ''.join(c if c.isalnum() else '_' for c in self.config_manager.config.name)
        extension = EXECUTABLE_EXTENSIONS.get(self.config_manager.config.target_os, "")
        
        default_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{safe_name}{extension}")
        self.output_path_input.setText(default_path)
    
    @pyqtSlot()
    def browse_output_path(self):
        """Browse for output file path."""
        # Get safe name for the executable
        safe_name = ''.join(c if c.isalnum() else '_' for c in self.config_manager.config.name)
        extension = EXECUTABLE_EXTENSIONS.get(self.config_manager.config.target_os, "")
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Launcher Executable",
            os.path.join(os.path.expanduser("~"), "Desktop", f"{safe_name}{extension}"),
            f"Executable Files (*{extension});;All Files (*)"
        )
        
        if file_path:
            # Ensure the path has the correct extension
            if not file_path.lower().endswith(extension.lower()):
                file_path += extension
            
            self.output_path_input.setText(file_path)
    
    @pyqtSlot()
    def start_build(self):
        """Start the build process."""
        # Validate configuration
        errors = self.config_manager.validate()
        if errors:
            error_msg = "The configuration has the following errors:\n\n"
            for field, message in errors.items():
                error_msg += f"• {message}\n"
            
            QMessageBox.critical(
                self,
                "Validation Error",
                error_msg
            )
            return
        
        # Check output path
        output_path = self.output_path_input.text()
        if not output_path:
            QMessageBox.critical(
                self,
                "Error",
                "Please specify an output path for the executable."
            )
            return
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to create output directory: {e}"
                )
                return
        
        # Show progress UI
        self.build_button.setEnabled(False)
        self.progress_group.setVisible(True)
        self.results_group.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Preparing build...")
        
        # Start build thread
        self.build_thread = BuildThread(self.config_manager, output_path)
        self.build_thread.progress_updated.connect(self.update_progress)
        self.build_thread.build_completed.connect(self.build_completed)
        self.build_thread.start()
    
    @pyqtSlot(str, int)
    def update_progress(self, message: str, progress: int):
        """
        Update build progress display.
        
        Args:
            message: Progress message
            progress: Progress percentage (0-100)
        """
        self.progress_label.setText(message)
        self.progress_bar.setValue(progress)
    
    @pyqtSlot(bool, str, str)
    def build_completed(self, success: bool, error: str, output_path: str):
        """
        Handle build completion.
        
        Args:
            success: Whether the build was successful
            error: Error message if build failed
            output_path: Path to the built executable
        """
        self.progress_group.setVisible(False)
        self.results_group.setVisible(True)
        
        if success:
            self.results_label.setText(
                f"<span style='color: green; font-weight: bold;'>Build completed successfully!</span><br><br>"
                f"Launcher executable created at:<br>{output_path}"
            )
            self.results_label.setTextFormat(Qt.RichText)
            self.open_folder_button.setEnabled(True)
            self.open_folder_button.setProperty("output_path", output_path)
        else:
            self.results_label.setText(
                f"<span style='color: red; font-weight: bold;'>Build failed!</span><br><br>"
                f"Error: {error}"
            )
            self.results_label.setTextFormat(Qt.RichText)
            self.open_folder_button.setEnabled(False)
    
    @pyqtSlot()
    def open_output_folder(self):
        """Open the folder containing the built executable."""
        output_path = self.open_folder_button.property("output_path")
        if output_path and os.path.exists(output_path):
            open_file_explorer(os.path.dirname(output_path))
    
    @pyqtSlot()
    def reset_build_ui(self):
        """Reset the build UI for a new build."""
        self.build_button.setEnabled(True)
        self.progress_group.setVisible(False)
        self.results_group.setVisible(False)
