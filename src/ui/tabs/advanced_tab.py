"""
Advanced settings tab for configuring validation files, target OS, and default locations.
"""

import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSlot

from src.builder.config_manager import ConfigManager
from src.utils.file_utils import get_common_game_directories, get_basename
from src.models.constants import DEFAULT_GAME_LOCATIONS

logger = logging.getLogger(__name__)

class AdvancedSettingsTab(QWidget):
    """Tab for configuring advanced launcher settings."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the advanced settings tab.
        
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
        title_label = QLabel("Advanced Settings")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        description_label = QLabel(
            "Configure advanced settings for your launcher. "
            "These settings affect how the launcher identifies the game folder and other behaviors."
        )
        description_label.setWordWrap(True)
        layout.addWidget(description_label)
        
        # Target OS group
        target_os_group = QGroupBox("Target Operating System")
        target_os_layout = QVBoxLayout(target_os_group)
        
        target_os_label = QLabel(
            "Select the operating system that the launcher will be built for. "
            "The launcher will only work on the selected platform."
        )
        target_os_label.setWordWrap(True)
        target_os_layout.addWidget(target_os_label)
        
        self.target_os_combo = QComboBox()
        self.target_os_combo.addItems(["Windows", "macOS", "Linux"])
        self.target_os_combo.currentIndexChanged.connect(self.on_target_os_changed)
        target_os_layout.addWidget(self.target_os_combo)
        
        layout.addWidget(target_os_group)
        
        # Validation files group
        validation_group = QGroupBox("Validation Files")
        validation_layout = QVBoxLayout(validation_group)
        
        validation_label = QLabel(
            "Validation files are used to verify that the selected folder is the correct game folder. "
            "The launcher will check for these files when a user selects a folder."
        )
        validation_label.setWordWrap(True)
        validation_layout.addWidget(validation_label)
        
        self.validation_table = QTableWidget(0, 1)
        self.validation_table.setHorizontalHeaderLabels(["File Path"])
        self.validation_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        validation_layout.addWidget(self.validation_table)
        
        validation_buttons = QHBoxLayout()
        
        add_validation_button = QPushButton("Add File")
        add_validation_button.clicked.connect(self.add_validation_file)
        validation_buttons.addWidget(add_validation_button)
        
        remove_validation_button = QPushButton("Remove Selected")
        remove_validation_button.clicked.connect(self.remove_validation_file)
        validation_buttons.addWidget(remove_validation_button)
        
        validation_layout.addLayout(validation_buttons)
        layout.addWidget(validation_group)
        
        # Default locations group
        locations_group = QGroupBox("Default Game Locations")
        locations_layout = QVBoxLayout(locations_group)
        
        locations_label = QLabel(
            "Default game locations help the launcher automatically find the game installation. "
            "Specify common installation paths for the game."
        )
        locations_label.setWordWrap(True)
        locations_layout.addWidget(locations_label)
        
        self.locations_table = QTableWidget(0, 1)
        self.locations_table.setHorizontalHeaderLabels(["Path"])
        self.locations_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        locations_layout.addWidget(self.locations_table)
        
        locations_buttons = QHBoxLayout()
        
        add_location_button = QPushButton("Add Location")
        add_location_button.clicked.connect(self.add_default_location)
        locations_buttons.addWidget(add_location_button)
        
        add_common_button = QPushButton("Add Common Locations")
        add_common_button.clicked.connect(self.add_common_locations)
        locations_buttons.addWidget(add_common_button)
        
        remove_location_button = QPushButton("Remove Selected")
        remove_location_button.clicked.connect(self.remove_default_location)
        locations_buttons.addWidget(remove_location_button)
        
        locations_layout.addLayout(locations_buttons)
        layout.addWidget(locations_group)
        
        # Help text
        help_group = QGroupBox("Help")
        help_layout = QVBoxLayout(help_group)
        
        help_text = (
            "<b>Target OS:</b> The launcher will only work on the selected operating system.<br><br>"
            "<b>Validation Files:</b> Relative paths to files that should exist in the game folder.<br>"
            "Example: <code>game.exe</code> or <code>data/config.ini</code><br><br>"
            "<b>Default Game Locations:</b> Paths where the launcher should look for the game.<br>"
            "These should be absolute paths specific to the target OS."
        )
        
        help_label = QLabel(help_text)
        help_label.setTextFormat(Qt.RichText)
        help_label.setWordWrap(True)
        help_layout.addWidget(help_label)
        
        layout.addWidget(help_group)
        
        # Fill UI with data
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
        # Set target OS
        target_os_map = {"windows": 0, "macos": 1, "linux": 2}
        self.target_os_combo.setCurrentIndex(
            target_os_map.get(self.config_manager.config.target_os.lower(), 0)
        )
        
        # Clear validation files table
        self.validation_table.setRowCount(0)
        
        # Fill validation files table
        for file_path in self.config_manager.config.validation_files:
            row = self.validation_table.rowCount()
            self.validation_table.insertRow(row)
            self.validation_table.setItem(row, 0, QTableWidgetItem(file_path))
        
        # Clear default locations table
        self.locations_table.setRowCount(0)
        
        # Fill default locations table
        for location in self.config_manager.config.default_locations:
            row = self.locations_table.rowCount()
            self.locations_table.insertRow(row)
            self.locations_table.setItem(row, 0, QTableWidgetItem(location))
    
    @pyqtSlot(int)
    def on_target_os_changed(self, index: int):
        """
        Handle target OS selection changed.
        
        Args:
            index: Selected index in the combo box
        """
        target_os_map = {0: "windows", 1: "macos", 2: "linux"}
        self.config_manager.config.target_os = target_os_map.get(index, "windows")
        self.config_manager.save()
    
    @pyqtSlot()
    def add_validation_file(self):
        """Add a new validation file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Validation File",
            "",
            "All Files (*)"
        )
        
        if file_path:
            # Get just the filename or relative path
            relative_path = get_basename(file_path)
            
            # Only add if not already in the list
            if relative_path not in self.config_manager.config.validation_files:
                # Add to configuration
                self.config_manager.config.add_validation_file(relative_path)
                
                # Add to table
                row = self.validation_table.rowCount()
                self.validation_table.insertRow(row)
                self.validation_table.setItem(row, 0, QTableWidgetItem(relative_path))
                
                # Save configuration
                self.config_manager.save()
    
    @pyqtSlot()
    def remove_validation_file(self):
        """Remove the selected validation file."""
        selected_rows = self.validation_table.selectionModel().selectedRows()
        if not selected_rows:
            selected_items = self.validation_table.selectedItems()
            if selected_items:
                selected_rows = list(set(item.row() for item in selected_items))
            else:
                return
        
        # Sort rows in descending order to avoid index issues when removing
        rows = sorted(set(index.row() for index in selected_rows), reverse=True)
        
        for row in rows:
            # Get the file path
            file_path = self.validation_table.item(row, 0).text()
            
            # Remove from configuration
            self.config_manager.config.remove_validation_file(file_path)
            
            # Remove from table
            self.validation_table.removeRow(row)
        
        # Save configuration
        self.config_manager.save()
    
    @pyqtSlot()
    def add_default_location(self):
        """Add a new default game location."""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Default Game Location",
            ""
        )
        
        if dir_path:
            # Only add if not already in the list
            if dir_path not in self.config_manager.config.default_locations:
                # Add to configuration
                self.config_manager.config.add_default_location(dir_path)
                
                # Add to table
                row = self.locations_table.rowCount()
                self.locations_table.insertRow(row)
                self.locations_table.setItem(row, 0, QTableWidgetItem(dir_path))
                
                # Save configuration
                self.config_manager.save()
    
    @pyqtSlot()
    def add_common_locations(self):
        """Add common game locations for the selected platform."""
        target_os = self.config_manager.config.target_os.lower()
        
        # Get common locations from constants or detect them
        common_locations = DEFAULT_GAME_LOCATIONS.get(target_os, [])
        
        # Add detected locations
        detected_locations = get_common_game_directories()
        
        # Combine all locations
        all_locations = list(set(common_locations + detected_locations))
        
        # Add each location if not already in the list
        added_count = 0
        for location in all_locations:
            if location not in self.config_manager.config.default_locations:
                # Add to configuration
                self.config_manager.config.add_default_location(location)
                
                # Add to table
                row = self.locations_table.rowCount()
                self.locations_table.insertRow(row)
                self.locations_table.setItem(row, 0, QTableWidgetItem(location))
                
                added_count += 1
        
        # Save configuration if any locations were added
        if added_count > 0:
            self.config_manager.save()
            QMessageBox.information(
                self,
                "Common Locations Added",
                f"Added {added_count} common game locations."
            )
        else:
            QMessageBox.information(
                self,
                "No New Locations",
                "No new common locations were found."
            )
    
    @pyqtSlot()
    def remove_default_location(self):
        """Remove the selected default location."""
        selected_rows = self.locations_table.selectionModel().selectedRows()
        if not selected_rows:
            selected_items = self.locations_table.selectedItems()
            if selected_items:
                selected_rows = list(set(item.row() for item in selected_items))
            else:
                return
        
        # Sort rows in descending order to avoid index issues when removing
        rows = sorted(set(index.row() for index in selected_rows), reverse=True)
        
        for row in rows:
            # Get the location
            location = self.locations_table.item(row, 0).text()
            
            # Remove from configuration
            self.config_manager.config.remove_default_location(location)
            
            # Remove from table
            self.locations_table.removeRow(row)
        
        # Save configuration
        self.config_manager.save()
