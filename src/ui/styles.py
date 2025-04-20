"""
UI styles and theme management for the application.
"""

import logging
from PyQt5.QtWidgets import QApplication, QWidget, QStyleFactory
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)

def setup_styles(widget: QWidget = None):
    """
    Set up application styles.
    
    Args:
        widget: Widget to apply styles to (or None for application-wide)
    """
    # Use Fusion style for a modern look
    app = QApplication.instance()  # Get the existing QApplication instance
    app.setStyle(QStyleFactory.create("Fusion"))

    # Set default font
    font = QFont("Segoe UI", 9)  # Windows default
    app.setFont(font)

    # Set color palette
    palette = QPalette()

    # Base colors
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(30, 30, 30))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(248, 248, 248))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(30, 30, 30))
    palette.setColor(QPalette.Text, QColor(30, 30, 30))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(30, 30, 30))

    # Highlight colors
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    # Link colors
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.LinkVisited, QColor(80, 80, 160))

    # Apply palette
    if widget:
        widget.setPalette(palette)
    else:
        app.setPalette(palette)

    # Apply stylesheet
    style_sheet = """
    /* QWidget */
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* QGroupBox */
    QGroupBox {
        font-weight: bold;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-top: 1ex;
        padding: 10px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 3px;
        margin-left: 5px;
    }
    
    /* QTabWidget */
    QTabWidget::pane {
        border: 1px solid #ccc;
        border-top: 0px;
        border-radius: 5px;
    }
    
    QTabBar::tab {
        background: #f0f0f0;
        border: 1px solid #ccc;
        border-bottom-color: #ccc;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        padding: 5px 10px;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background: #fff;
        border-bottom-color: #fff;
    }
    
    QTabBar::tab:!selected {
        margin-top: 2px;
    }
    
    /* QPushButton */
    QPushButton {
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 5px 15px;
        outline: none;
    }
    
    QPushButton:hover {
        background-color: #e0e0e0;
        border: 1px solid #aaa;
    }
    
    QPushButton:pressed {
        background-color: #d0d0d0;
    }
    
    QPushButton:disabled {
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        color: #aaa;
    }
    
    /* QLineEdit, QTextEdit */
    QLineEdit, QTextEdit {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 2px 5px;
        background-color: white;
        selection-background-color: #2a82da;
    }
    
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #2a82da;
    }
    
    /* QComboBox */
    QComboBox {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 2px 5px;
        background-color: white;
        min-width: 6em;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #ccc;
    }
    
    QComboBox:on {
        border: 1px solid #2a82da;
    }
    
    /* QTableWidget */
    QTableWidget {
        border: 1px solid #ccc;
        gridline-color: #ddd;
        selection-background-color: #2a82da;
        selection-color: white;
    }
    
    QTableWidget QHeaderView::section {
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-left: 0px;
        padding: 5px;
        font-weight: bold;
    }
    
    QTableWidget QHeaderView::section:first {
        border-left: 1px solid #ccc;
    }
    
    /* QProgressBar */
    QProgressBar {
        border: 1px solid #ccc;
        border-radius: 4px;
        text-align: center;
        background-color: #f0f0f0;
    }
    
    QProgressBar::chunk {
        background-color: #2a82da;
        width: 1px;
    }
    
    /* QScrollBar */
    QScrollBar:vertical {
        border: 1px solid #ccc;
        background: #f0f0f0;
        width: 15px;
        margin: 22px 0 22px 0;
    }
    
    QScrollBar::handle:vertical {
        background: #aaa;
        min-height: 20px;
    }
    
    QScrollBar::add-line:vertical {
        border: 1px solid #ccc;
        background: #f0f0f0;
        height: 20px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    
    QScrollBar::sub-line:vertical {
        border: 1px solid #ccc;
        background: #f0f0f0;
        height: 20px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    
    /* QStatusBar */
    QStatusBar {
        background-color: #f0f0f0;
        border-top: 1px solid #ccc;
    }
    
    QStatusBar::item {
        border: none;
    }
    """

    if widget:
        widget.setStyleSheet(style_sheet)
    else:
        app.setStyleSheet(style_sheet)

    logger.debug("Applied application styles")


def setup_dark_theme(widget: QWidget = None):
    """
    Set up dark theme.

    Args:
        widget: Widget to apply theme to (or None for application-wide)
    """
    # Use Fusion style for a modern look
    app = QApplication.instance()  # Get the existing QApplication instance
    app.setStyle(QStyleFactory.create("Fusion"))

    # Set default font
    font = QFont("Segoe UI", 9)  # Windows default
    app.setFont(font)

    # Create dark palette
    palette = QPalette()

    # Base colors
    dark_color = QColor(53, 53, 53)
    palette.setColor(QPalette.Window, dark_color)
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(42, 42, 42))
    palette.setColor(QPalette.ToolTipBase, QColor(35, 35, 35))
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, dark_color)
    palette.setColor(QPalette.ButtonText, Qt.white)

    # Highlight colors
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.white)

    # Disabled colors
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128, 128, 128))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(128, 128, 128))

    # Link colors
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.LinkVisited, QColor(130, 130, 200))

    # Apply palette
    if widget:
        widget.setPalette(palette)
    else:
        app.setPalette(palette)

    # Apply stylesheet for dark theme
    style_sheet = """
    /* QWidget */
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* QGroupBox */
    QGroupBox {
        font-weight: bold;
        border: 1px solid #555;
        border-radius: 5px;
        margin-top: 1ex;
        padding: 10px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 3px;
        margin-left: 5px;
    }
    
    /* QTabWidget */
    QTabWidget::pane {
        border: 1px solid #555;
        border-top: 0px;
        border-radius: 5px;
    }
    
    QTabBar::tab {
        background: #353535;
        border: 1px solid #555;
        border-bottom-color: #555;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        padding: 5px 10px;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background: #252525;
        border-bottom-color: #252525;
    }
    
    QTabBar::tab:!selected {
        margin-top: 2px;
    }
    
    /* QPushButton */
    QPushButton {
        background-color: #353535;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 5px 15px;
        outline: none;
    }
    
    QPushButton:hover {
        background-color: #454545;
        border: 1px solid #666;
    }
    
    QPushButton:pressed {
        background-color: #252525;
    }
    
    QPushButton:disabled {
        background-color: #353535;
        border: 1px solid #444;
        color: #666;
    }
    
    /* QLineEdit, QTextEdit */
    QLineEdit, QTextEdit {
        border: 1px solid #555;
        border-radius: 4px;
        padding: 2px 5px;
        background-color: #252525;
        selection-background-color: #2a82da;
    }
    
    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #2a82da;
    }
    
    /* QComboBox */
    QComboBox {
        border: 1px solid #555;
        border-radius: 4px;
        padding: 2px 5px;
        background-color: #252525;
        min-width: 6em;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #555;
    }
    
    QComboBox:on {
        border: 1px solid #2a82da;
    }
    
    /* QTableWidget */
    QTableWidget {
        border: 1px solid #555;
        gridline-color: #444;
        selection-background-color: #2a82da;
        selection-color: white;
    }
    
    QTableWidget QHeaderView::section {
        background-color: #353535;
        border: 1px solid #555;
        border-left: 0px;
        padding: 5px;
        font-weight: bold;
    }
    
    QTableWidget QHeaderView::section:first {
        border-left: 1px solid #555;
    }
    
    /* QProgressBar */
    QProgressBar {
        border: 1px solid #555;
        border-radius: 4px;
        text-align: center;
        background-color: #252525;
    }
    
    QProgressBar::chunk {
        background-color: #2a82da;
        width: 1px;
    }
    
    /* QScrollBar */
    QScrollBar:vertical {
        border: 1px solid #555;
        background: #353535;
        width: 15px;
        margin: 22px 0 22px 0;
    }
    
    QScrollBar::handle:vertical {
        background: #555;
        min-height: 20px;
    }
    
    QScrollBar::add-line:vertical {
        border: 1px solid #555;
        background: #353535;
        height: 20px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    
    QScrollBar::sub-line:vertical {
        border: 1px solid #555;
        background: #353535;
        height: 20px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    
    /* QStatusBar */
    QStatusBar {
        background-color: #353535;
        border-top: 1px solid #555;
    }
    
    QStatusBar::item {
        border: none;
    }
    """

    if widget:
        widget.setStyleSheet(style_sheet)
    else:
        app.setStyleSheet(style_sheet)

    logger.debug("Applied dark theme")