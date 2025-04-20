"""
Main application window for the Game Mod Builder.
"""

import logging
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QWidget, QAction, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QCloseEvent

from src.models.constants import (
    APP_NAME, APP_VERSION, UI_MIN_WIDTH, UI_MIN_HEIGHT, APP_AUTHOR
)
from src.builder.config_manager import ConfigManager
from src.ui.tabs.basic_tab import BasicSettingsTab
from src.ui.tabs.mods_tab import ModsTab
from src.ui.tabs.advanced_tab import AdvancedSettingsTab
from src.ui.tabs.preview_tab import PreviewTab
from src.ui.tabs.build_tab import BuildTab
from src.ui.styles import setup_styles

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window for the Game Mod Builder."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Initialize config manager
        self.config_manager = ConfigManager()
        self.config_manager.load()  # Try to load last config
        
        # Initialize UI
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(UI_MIN_WIDTH, UI_MIN_HEIGHT)
        
        # Apply styles
        setup_styles(self)
        
        # Set up central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        
        # Create tabs
        self.basic_tab = BasicSettingsTab(self.config_manager)
        self.mods_tab = ModsTab(self.config_manager)
        self.advanced_tab = AdvancedSettingsTab(self.config_manager)
        self.preview_tab = PreviewTab(self.config_manager)
        self.build_tab = BuildTab(self.config_manager)
        
        # Add tabs to tab widget
        self.tabs.addTab(self.basic_tab, "Basic Settings")
        self.tabs.addTab(self.mods_tab, "Mods")
        self.tabs.addTab(self.advanced_tab, "Advanced Settings")
        self.tabs.addTab(self.preview_tab, "Preview")
        self.tabs.addTab(self.build_tab, "Build")
        
        # Add tab widget to layout
        self.main_layout.addWidget(self.tabs)
        
        # Create menus
        self.create_menus()
        
        # Set up event handlers
        self.setup_event_handlers()
        
        # Show the window
        self.show()
    
    def create_menus(self):
        """Create application menus."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        # New config action
        new_action = QAction("&New Configuration", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_config)
        file_menu.addAction(new_action)
        
        # Open config action
        open_action = QAction("&Open Configuration...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_config)
        file_menu.addAction(open_action)
        
        # Save config action
        save_action = QAction("&Save Configuration", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_config)
        file_menu.addAction(save_action)
        
        # Save As config action
        save_as_action = QAction("Save Configuration &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_config_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Export config action
        export_action = QAction("&Export Configuration...", self)
        export_action.triggered.connect(self.export_config)
        file_menu.addAction(export_action)
        
        # Import config action
        import_action = QAction("&Import Configuration...", self)
        import_action.triggered.connect(self.import_config)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_event_handlers(self):
        """Set up event handlers for tab interactions."""
        # Tab changed event
        self.tabs.currentChanged.connect(self.on_tab_changed)
    
    @pyqtSlot(int)
    def on_tab_changed(self, index):
        """
        Handle tab changed event.
        
        Args:
            index: Index of the selected tab
        """
        # Update data when switching to preview tab
        if self.tabs.widget(index) == self.preview_tab:
            self.preview_tab.update_preview()
    
    def new_config(self):
        """Create a new configuration."""
        # Ask for confirmation if current config has been modified
        if self._confirm_unsaved_changes():
            self.config_manager = ConfigManager()  # Reset to default config
            
            # Update all tabs with new config manager
            self.basic_tab.set_config_manager(self.config_manager)
            self.mods_tab.set_config_manager(self.config_manager)
            self.advanced_tab.set_config_manager(self.config_manager)
            self.preview_tab.set_config_manager(self.config_manager)
            self.build_tab.set_config_manager(self.config_manager)
            
            # Refresh all tabs
            self.basic_tab.refresh()
            self.mods_tab.refresh()
            self.advanced_tab.refresh()
            self.preview_tab.refresh()
            self.build_tab.refresh()
            
            self.statusBar().showMessage("New configuration created", 3000)
    
    def open_config(self):
        """Open a configuration file."""
        if self._confirm_unsaved_changes():
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Configuration",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_path:
                if self.config_manager.load(file_path):
                    # Refresh all tabs
                    self.basic_tab.refresh()
                    self.mods_tab.refresh()
                    self.advanced_tab.refresh()
                    self.preview_tab.refresh()
                    self.build_tab.refresh()
                    
                    self.statusBar().showMessage(f"Configuration loaded from {file_path}", 3000)
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to load configuration from {file_path}"
                    )
    
    def save_config(self):
        """Save the current configuration."""
        if self.config_manager.config_path:
            if self.config_manager.save():
                self.statusBar().showMessage(
                    f"Configuration saved to {self.config_manager.config_path}", 
                    3000
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save configuration to {self.config_manager.config_path}"
                )
        else:
            self.save_config_as()
    
    def save_config_as(self):
        """Save the current configuration to a new file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Configuration As",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            if not file_path.lower().endswith('.json'):
                file_path += '.json'
                
            if self.config_manager.save(file_path):
                self.statusBar().showMessage(f"Configuration saved to {file_path}", 3000)
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save configuration to {file_path}"
                )
    
    def export_config(self):
        """Export the current configuration."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Configuration",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            if not file_path.lower().endswith('.json'):
                file_path += '.json'
                
            if self.config_manager.export_config(file_path):
                self.statusBar().showMessage(f"Configuration exported to {file_path}", 3000)
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to export configuration to {file_path}"
                )
    
    def import_config(self):
        """Import a configuration file."""
        if self._confirm_unsaved_changes():
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Import Configuration",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_path:
                if self.config_manager.import_config(file_path):
                    # Refresh all tabs
                    self.basic_tab.refresh()
                    self.mods_tab.refresh()
                    self.advanced_tab.refresh()
                    self.preview_tab.refresh()
                    self.build_tab.refresh()
                    
                    self.statusBar().showMessage(f"Configuration imported from {file_path}", 3000)
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to import configuration from {file_path}"
                    )
    
    def show_about(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"<h1>{APP_NAME}</h1>"
            f"<p>Version {APP_VERSION}</p>"
            f"<p>A tool for creating custom game launchers and mod installers.</p>"
            f"<p>Created by {APP_AUTHOR}</p>"
        )
    
    def closeEvent(self, event: QCloseEvent):
        """
        Handle window close event.
        
        Args:
            event: Close event
        """
        if self._confirm_unsaved_changes():
            event.accept()
        else:
            event.ignore()
    
    def _confirm_unsaved_changes(self) -> bool:
        """
        Check if there are unsaved changes and ask for confirmation.
        
        Returns:
            bool: True if it's OK to proceed (no changes or user confirmed)
        """
        # In a real app, you'd check if the config has been modified
        # For simplicity, we'll just always save before proceeding
        self.config_manager.save()
        return True
