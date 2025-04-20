"""
Mods tab for managing mod entries in the configuration.
"""

import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QLabel, QGroupBox, QMessageBox, QCheckBox,
    QStyledItemDelegate, QTextEdit
)
from PyQt5.QtCore import Qt, pyqtSlot, QTimer

from src.builder.config_manager import ConfigManager
from src.models.config_model import ModConfig
from src.models.constants import (
    DEFAULT_MOD_NAME, DEFAULT_MOD_TARGET_PATH,
    DEFAULT_MOD_DOWNLOAD_URL, DEFAULT_MOD_DESCRIPTION
)

logger = logging.getLogger(__name__)

class ModTableDelegate(QStyledItemDelegate):
    """Custom delegate for mod table items."""

    def createEditor(self, parent, option, index):
        """
        Create editor widget for table cell.

        Args:
            parent: Parent widget
            option: Style options
            index: Model index

        Returns:
            QWidget: Editor widget
        """
        column = index.column()
        if column == 3:  # Description column
            editor = QTextEdit(parent)
            return editor
        else:
            return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """
        Set editor data from model.

        Args:
            editor: Editor widget
            index: Model index
        """
        column = index.column()
        if column == 3:  # Description column
            editor.setPlainText(index.model().data(index, Qt.EditRole))
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        """
        Set model data from editor.

        Args:
            editor: Editor widget
            model: Data model
            index: Model index
        """
        column = index.column()
        if column == 3:  # Description column
            model.setData(index, editor.toPlainText(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)

class ModsTab(QWidget):
    """Tab for managing mod entries in the configuration."""

    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the mods tab.

        Args:
            config_manager: Configuration manager instance
        """
        super().__init__()
        self.config_manager = config_manager

        # Flag to track programmatic resizing
        self._is_programmatic_resize = False

        # Define column width percentages (total should be 100%)
        self.column_percentages = {
            "Name": 20,
            "Target Path": 20,
            "Download URL": 20,
            "Description": 30,
            "Required": 10
        }

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title and description
        title_label = QLabel("Mod Management")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        description_label = QLabel(
            "Add, edit, and remove mods for your launcher. "
            "Each mod requires a name, target path, and download URL."
        )
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # Mods table
        self.mods_group = QGroupBox("Mods")
        mods_layout = QVBoxLayout(self.mods_group)

        self.mods_table = QTableWidget(0, 5)  # Name, Target Path, URL, Description, Required

        # Set header labels - make sure they are clear and fully visible
        self.mods_table.setHorizontalHeaderLabels(self.column_percentages.keys())

        # Configure header
        header = self.mods_table.horizontalHeader()
        header.setMinimumHeight(30)
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setStretchLastSection(False)

        # Set initial column behavior - all resizable by user
        for i in range(self.mods_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Interactive)

        # Connect to resize events to adjust column widths
        self.mods_table.horizontalHeader().sectionResized.connect(self.on_section_resized)

        # Set custom delegate for better editing
        self.mods_table.setItemDelegate(ModTableDelegate())

        # Connect signals
        self.mods_table.itemChanged.connect(self.on_table_item_changed)

        mods_layout.addWidget(self.mods_table)

        # Buttons for managing mods
        buttons_layout = QHBoxLayout()

        self.add_mod_button = QPushButton("Add Mod")
        self.add_mod_button.clicked.connect(self.add_mod)
        buttons_layout.addWidget(self.add_mod_button)

        self.remove_mod_button = QPushButton("Remove Selected")
        self.remove_mod_button.clicked.connect(self.remove_selected_mod)
        buttons_layout.addWidget(self.remove_mod_button)

        buttons_layout.addStretch()

        mods_layout.addLayout(buttons_layout)
        layout.addWidget(self.mods_group)

        # Help text
        help_group = QGroupBox("Help")
        help_layout = QVBoxLayout(help_group)

        help_text = (
            "<b>Target Path:</b> Relative path within the game folder where the mod will be installed.<br>"
            "Example: <code>mods/</code> or <code>data/textures/</code><br><br>"
            "<b>Download URL:</b> Direct download link for the mod ZIP file.<br>"
            "Supports Google Drive, Dropbox, and any other direct download links.<br><br>"
            "<b>Required:</b> If checked, the mod will be installed automatically and cannot be skipped."
        )

        help_label = QLabel(help_text)
        help_label.setTextFormat(Qt.RichText)
        help_label.setWordWrap(True)
        help_layout.addWidget(help_label)

        layout.addWidget(help_group)

        # Fill table with data
        self.refresh()

    def on_section_resized(self, logical_index, old_size, new_size):
        """
        Handle manual column resize and update stored percentages.

        This allows the user to resize columns and have them maintain proportions.
        """
        # Skip updating percentages if the resize was programmatic
        if self._is_programmatic_resize:
            return

        if not self.mods_table.isVisible():
            return

        table_width = self.mods_table.viewport().width()

        if table_width > 0:
            # Update the percentages based on new column widths
            column_keys = list(self.column_percentages.keys())
            for i, key in enumerate(column_keys):
                self.column_percentages[key] = int(100 * self.mods_table.columnWidth(i) / table_width)

    def adjust_column_widths(self):
        """Adjust column widths based on percentages of the table width."""
        # Set the programmatic resize flag
        self._is_programmatic_resize = True

        try:
            table_width = self.mods_table.viewport().width()

            # Skip if the table has no width yet
            if table_width <= 0:
                return

            # Calculate and set the column widths
            for i, percentage in enumerate(self.column_percentages.values()):
                self.mods_table.setColumnWidth(i, int(table_width * percentage / 100))
        finally:
            # Clear the flag when done
            self._is_programmatic_resize = False

    def set_config_manager(self, config_manager: ConfigManager):
        """
        Set a new configuration manager.

        Args:
            config_manager: New configuration manager instance
        """
        self.config_manager = config_manager

    def refresh(self):
        """Refresh the UI with current configuration data."""
        # Disconnect signals temporarily to avoid triggering updates
        self.mods_table.blockSignals(True)

        # Clear the table
        self.mods_table.setRowCount(0)

        # Fill with current mods
        for mod in self.config_manager.config.mods:
            self.add_mod_to_table(mod)

        # Reconnect signals
        self.mods_table.blockSignals(False)

    def add_mod_to_table(self, mod: ModConfig):
        """
        Add a mod to the table.

        Args:
            mod: Mod configuration to add
        """
        row = self.mods_table.rowCount()
        self.mods_table.insertRow(row)

        # Set mod data in table
        self.mods_table.setItem(row, 0, QTableWidgetItem(mod.name))
        self.mods_table.setItem(row, 1, QTableWidgetItem(mod.target_path))
        self.mods_table.setItem(row, 2, QTableWidgetItem(mod.download_url))
        self.mods_table.setItem(row, 3, QTableWidgetItem(mod.description))

        # Create checkbox for required status
        cell_widget = QWidget()
        layout = QHBoxLayout(cell_widget)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setAlignment(Qt.AlignCenter)

        checkbox = QCheckBox()
        checkbox.setChecked(mod.is_required)
        checkbox.stateChanged.connect(lambda state, r=row: self.on_required_changed(r, state))

        layout.addWidget(checkbox)
        self.mods_table.setCellWidget(row, 4, cell_widget)

        # Store mod ID in first column item for reference
        self.mods_table.item(row, 0).setData(Qt.UserRole, mod.id)

    @pyqtSlot()
    def add_mod(self):
        """Add a new mod to the configuration."""
        # Create new mod with default values
        new_mod = ModConfig(
            name=DEFAULT_MOD_NAME,
            target_path=DEFAULT_MOD_TARGET_PATH,
            download_url=DEFAULT_MOD_DOWNLOAD_URL,
            description=DEFAULT_MOD_DESCRIPTION,
            is_required=False
        )

        # Add to configuration
        self.config_manager.config.add_mod(new_mod)

        # Add to table
        self.add_mod_to_table(new_mod)

        # Save configuration
        self.config_manager.save()

    @pyqtSlot()
    def remove_selected_mod(self):
        """Remove the selected mod from the configuration."""
        selected_indices = self.mods_table.selectionModel().selectedRows()

        if selected_indices:
            # If rows are selected, get their indices
            row_indices = [index.row() for index in selected_indices]
        else:
            # If individual cells are selected, get their row indices
            selected_items = self.mods_table.selectedItems()
            if selected_items:
                row_indices = list(set(item.row() for item in selected_items))
            else:
                return  # Nothing selected

        # Confirm deletion
        if row_indices:
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to remove {len(row_indices)} mod(s)?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                # Sort rows in descending order to avoid index issues when removing
                rows = sorted(row_indices, reverse=True)

                for row in rows:
                    # Get the mod ID
                    mod_id = self.mods_table.item(row, 0).data(Qt.UserRole)

                    # Remove from configuration
                    self.config_manager.config.remove_mod(mod_id)

                    # Remove from table
                    self.mods_table.removeRow(row)

                # Save configuration
                self.config_manager.save()

    @pyqtSlot(QTableWidgetItem)
    def on_table_item_changed(self, item: QTableWidgetItem):
        """
        Handle item changed in the table.

        Args:
            item: Changed table item
        """
        row = item.row()
        column = item.column()

        # Get the mod ID
        mod_id = self.mods_table.item(row, 0).data(Qt.UserRole)

        # Find the mod in the configuration
        mod = next((m for m in self.config_manager.config.mods if m.id == mod_id), None)
        if not mod:
            logger.warning(f"Mod with ID {mod_id} not found in configuration")
            return

        # Update mod data based on column
        if column == 0:  # Name
            mod.name = item.text()
        elif column == 1:  # Target Path
            mod.target_path = item.text()
        elif column == 2:  # Download URL
            mod.download_url = item.text()
        elif column == 3:  # Description
            mod.description = item.text()

        # Save configuration
        self.config_manager.save()

    @pyqtSlot(int, int)
    def on_required_changed(self, row: int, state: int):
        """
        Handle required checkbox state changed.

        Args:
            row: Table row
            state: Checkbox state
        """
        # Get the mod ID
        mod_id = self.mods_table.item(row, 0).data(Qt.UserRole)

        # Find the mod in the configuration
        mod = next((m for m in self.config_manager.config.mods if m.id == mod_id), None)
        if not mod:
            logger.warning(f"Mod with ID {mod_id} not found in configuration")
            return

        # Update required state
        mod.is_required = (state == Qt.Checked)

        # Save configuration
        self.config_manager.save()

    def showEvent(self, event):
        """Handle show events to adjust column widths when tab becomes visible."""
        super().showEvent(event)
        self.adjust_column_widths()

    def resizeEvent(self, event):
        """Handle resize events to adjust column widths."""
        super().resizeEvent(event)
        self.adjust_column_widths()