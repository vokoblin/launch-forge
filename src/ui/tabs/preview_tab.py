"""
Preview tab for showing a preview of the launcher.
"""

import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton,
    QHBoxLayout, QScrollArea, QFrame, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QFont

from src.builder.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class PreviewTab(QWidget):
    """Tab for showing a preview of the launcher."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the preview tab.
        
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
        title_label = QLabel("Launcher Preview")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        description_label = QLabel(
            "Preview how your launcher will look to users. "
            "This is a visual representation of the launcher that will be created."
        )
        description_label.setWordWrap(True)
        layout.addWidget(description_label)
        
        # Preview scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Preview container
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        
        # Create the preview components
        self.setup_preview_components()
        
        # Set the container as the scroll area's widget
        scroll_area.setWidget(self.preview_container)
        layout.addWidget(scroll_area)
        
        # Update button
        update_button = QPushButton("Update Preview")
        update_button.clicked.connect(self.update_preview)
        layout.addWidget(update_button, alignment=Qt.AlignRight)
        
        # Help text
        help_group = QGroupBox("Help")
        help_layout = QVBoxLayout(help_group)
        
        help_text = (
            "<b>Preview:</b> This is a visual representation of how your launcher will look.<br>"
            "The actual launcher may have slight visual differences depending on the operating system.<br><br>"
            "<b>Update Preview:</b> Click this button to refresh the preview with your latest changes."
        )
        
        help_label = QLabel(help_text)
        help_label.setTextFormat(Qt.RichText)
        help_label.setWordWrap(True)
        help_layout.addWidget(help_label)
        
        layout.addWidget(help_group)
    
    def setup_preview_components(self):
        """Set up the preview components."""
        # Clear existing components
        while self.preview_layout.count():
            item = self.preview_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create a mock-up of the launcher UI
        self.launcher_frame = QFrame()
        self.launcher_frame.setFrameShape(QFrame.StyledPanel)
        self.launcher_frame.setFrameShadow(QFrame.Raised)
        self.launcher_frame.setStyleSheet(
            "QFrame { background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 5px; }"
        )
        
        launcher_layout = QVBoxLayout(self.launcher_frame)
        launcher_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(self.config_manager.config.name)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(title_label)
        
        about_button = QPushButton("About")
        about_button.setEnabled(False)
        header_layout.addWidget(about_button, alignment=Qt.AlignRight)
        
        launcher_layout.addLayout(header_layout)
        
        # Description
        if self.config_manager.config.description:
            desc_label = QLabel(self.config_manager.config.description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #666; margin-bottom: 10px;")
            launcher_layout.addWidget(desc_label)
        
        # Game path section
        path_group = QGroupBox("Game Location")
        path_layout = QVBoxLayout(path_group)
        
        path_label = QLabel("Game found at: C:\\Program Files\\SampleGame")
        path_layout.addWidget(path_label)
        
        select_path_btn = QPushButton("Select Game Folder")
        select_path_btn.setEnabled(False)
        path_layout.addWidget(select_path_btn)
        
        launcher_layout.addWidget(path_group)
        
        # Mods section
        mods_group = QGroupBox("Mods")
        mods_layout = QVBoxLayout(mods_group)
        
        mods_list = QListWidget()
        
        # Add mods to the list
        for mod in self.config_manager.config.mods:
            item = QListWidgetItem(f"{mod.name} - Not Installed")
            item.setIcon(QIcon.fromTheme("dialog-error"))
            mods_list.addItem(item)
        
        if not self.config_manager.config.mods:
            mods_list.addItem("No mods configured")
        
        mods_layout.addWidget(mods_list)
        
        # Progress bar (hidden initially)
        progress_group = QGroupBox("Progress")
        progress_group.setVisible(False)
        
        launcher_layout.addWidget(mods_group)
        launcher_layout.addWidget(progress_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        update_btn = QPushButton("Update/Install Mods")
        buttons_layout.addWidget(update_btn)
        
        play_btn = QPushButton("Play Game")
        buttons_layout.addWidget(play_btn)
        
        launcher_layout.addLayout(buttons_layout)
        
        # Status bar
        status_bar = QLabel("Ready")
        status_bar.setStyleSheet("color: #666; font-size: 8pt;")
        launcher_layout.addWidget(status_bar, alignment=Qt.AlignRight)
        
        # Add the launcher frame to the preview layout
        self.preview_layout.addWidget(self.launcher_frame)
        
        # Add explanation
        explanation_label = QLabel(
            "This preview shows how the launcher will appear to users. "
            "The launcher will automatically detect the game folder, "
            "download and install mods, and provide a button to launch the game."
        )
        explanation_label.setWordWrap(True)
        explanation_label.setStyleSheet("margin-top: 10px; color: #666;")
        self.preview_layout.addWidget(explanation_label)
        
        # Add launcher functionality description
        functionality_group = QGroupBox("Launcher Functionality")
        functionality_layout = QVBoxLayout(functionality_group)
        
        functionality_text = (
            f"<p>Your launcher will:</p>"
            f"<ol>"
            f"<li>Allow users to select or auto-detect the game folder</li>"
            f"<li>Validate the game folder using {len(self.config_manager.config.validation_files)} validation files</li>"
            f"<li>Download and install {len(self.config_manager.config.mods)} mod(s)</li>"
            f"<li>Track which mods are installed</li>"
            f"<li>Launch the game executable: <b>{self.config_manager.config.game_exe}</b></li>"
            f"</ol>"
            f"<p>Users will see the launcher name: <b>{self.config_manager.config.name}</b></p>"
            f"<p>The launcher will download {len(self.config_manager.config.mods)} mod(s) to their specified target paths.</p>"
        )
        
        functionality_label = QLabel(functionality_text)
        functionality_label.setTextFormat(Qt.RichText)
        functionality_label.setWordWrap(True)
        functionality_layout.addWidget(functionality_label)
        
        self.preview_layout.addWidget(functionality_group)
    
    def set_config_manager(self, config_manager: ConfigManager):
        """
        Set a new configuration manager.
        
        Args:
            config_manager: New configuration manager instance
        """
        self.config_manager = config_manager
    
    def refresh(self):
        """Refresh the UI with current configuration data."""
        self.update_preview()
    
    @pyqtSlot()
    def update_preview(self):
        """Update the preview with current configuration data."""
        self.setup_preview_components()
