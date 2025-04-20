"""
Basic settings tab for configuring launcher name, description, and other basic settings.
"""

import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QGroupBox, QLabel, QHBoxLayout, QPushButton, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSlot

from src.builder.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class BasicSettingsTab(QWidget):
    """Tab for configuring basic launcher settings."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the basic settings tab.
        
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
        title_label = QLabel("Basic Settings")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        description_label = QLabel(
            "Configure the basic settings for your launcher. "
            "These settings will be visible to users when they run the launcher."
        )
        description_label.setWordWrap(True)
        layout.addWidget(description_label)
        
        # Basic settings group
        self.settings_group = QGroupBox("Launcher Information")
        settings_layout = QFormLayout(self.settings_group)
        
        # Launcher name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter launcher name")
        self.name_input.textChanged.connect(self.on_name_changed)
        settings_layout.addRow("Launcher Name:", self.name_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter launcher description")
        self.description_input.textChanged.connect(self.on_description_changed)
        self.description_input.setMaximumHeight(100)
        settings_layout.addRow("Description:", self.description_input)
        
        # Game executable
        game_exe_layout = QHBoxLayout()
        
        self.game_exe_input = QLineEdit()
        self.game_exe_input.setPlaceholderText("Path to game executable (e.g., game.exe)")
        self.game_exe_input.textChanged.connect(self.on_game_exe_changed)
        game_exe_layout.addWidget(self.game_exe_input)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_game_exe)
        game_exe_layout.addWidget(browse_button)
        
        settings_layout.addRow("Game Executable:", game_exe_layout)
        
        # Version
        self.version_input = QLineEdit()
        self.version_input.setPlaceholderText("e.g., 1.0.0")
        self.version_input.textChanged.connect(self.on_version_changed)
        settings_layout.addRow("Version:", self.version_input)
        
        layout.addWidget(self.settings_group)
        
        # Help text
        help_group = QGroupBox("Help")
        help_layout = QVBoxLayout(help_group)
        
        help_text = (
            "<b>Launcher Name:</b> Name shown in the launcher title bar.<br><br>"
            "<b>Description:</b> Brief description of what your mod pack does.<br><br>"
            "<b>Game Executable:</b> Relative path to the game's executable file within the game folder.<br>"
            "Example: <code>game.exe</code> or <code>bin/game.exe</code><br><br>"
            "<b>Version:</b> Version number for your mod launcher."
        )
        
        help_label = QLabel(help_text)
        help_label.setTextFormat(Qt.RichText)
        help_label.setWordWrap(True)
        help_layout.addWidget(help_label)
        
        layout.addWidget(help_group)
        
        # Stretch to fill remaining space
        layout.addStretch()
        
        # Fill fields with current data
        self.refresh()
    
    def set_config_manager(self, config_manager: ConfigManager):
        """
        Set a new configuration manager.
        
        Args:
            config_manager: New configuration manager instance
        """
        self.config_manager = config_manager
    
    def refresh(self):
        """Refresh the UI with current configuration data."""
        # Block signals temporarily to avoid triggering updates
        self.name_input.blockSignals(True)
        self.description_input.blockSignals(True)
        self.game_exe_input.blockSignals(True)
        self.version_input.blockSignals(True)
        
        # Update fields
        self.name_input.setText(self.config_manager.config.name)
        self.description_input.setText(self.config_manager.config.description)
        self.game_exe_input.setText(self.config_manager.config.game_exe)
        self.version_input.setText(self.config_manager.config.version)
        
        # Unblock signals
        self.name_input.blockSignals(False)
        self.description_input.blockSignals(False)
        self.game_exe_input.blockSignals(False)
        self.version_input.blockSignals(False)
    
    @pyqtSlot(str)
    def on_name_changed(self, text: str):
        """
        Handle launcher name changed.
        
        Args:
            text: New name text
        """
        self.config_manager.config.name = text
        self.config_manager.save()
    
    @pyqtSlot()
    def on_description_changed(self):
        """Handle launcher description changed."""
        self.config_manager.config.description = self.description_input.toPlainText()
        self.config_manager.save()
    
    @pyqtSlot(str)
    def on_game_exe_changed(self, text: str):
        """
        Handle game executable path changed.
        
        Args:
            text: New path text
        """
        self.config_manager.config.game_exe = text
        
        # If this is the first validation file, update it as well
        if (not self.config_manager.config.validation_files or 
            (len(self.config_manager.config.validation_files) == 1 and 
             self.config_manager.config.validation_files[0] != text)):
            
            # Remove old validation file
            if self.config_manager.config.validation_files:
                self.config_manager.config.validation_files.clear()
            
            # Add new validation file
            if text:
                self.config_manager.config.validation_files.append(text)
        
        self.config_manager.save()
    
    @pyqtSlot(str)
    def on_version_changed(self, text: str):
        """
        Handle version changed.
        
        Args:
            text: New version text
        """
        self.config_manager.config.version = text
        self.config_manager.save()
    
    @pyqtSlot()
    def browse_game_exe(self):
        """Browse for game executable file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Game Executable",
            "",
            "Executable Files (*.exe);;All Files (*)"
        )
        
        if file_path:
            # Extract just the filename as we need a relative path
            file_name = file_path.split('/')[-1]
            self.game_exe_input.setText(file_name)
