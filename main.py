import sys
import json
import os
import glob
import re
from datetime import datetime
import pyperclip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                            QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
                            QComboBox, QMessageBox, QFileDialog, QSplitter,
                            QGroupBox, QHeaderView, QCheckBox, QFrame, QScrollArea, QSizePolicy,
                            QStylePainter, QStyleOptionButton, QStyle, QProxyStyle)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QPen, QLinearGradient
from PyQt6.QtWidgets import QListView # Added for the specific fix

CONFIGS_DIR = os.path.join(os.getcwd(), "configs")
os.makedirs(CONFIGS_DIR, exist_ok=True)

# Custom style to fix dropdown menu background on macOS
class DarkProxyStyle(QProxyStyle):
    def __init__(self, style=None):
        super().__init__(style)
        
    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QStyle.StyleHint.SH_ComboBox_Popup:
            # Return 0 to disable the native macOS popup
            return 0
        return super().styleHint(hint, option, widget, returnData)

class ModernCard(QFrame):
    """Modern card widget with rounded corners and shadow effect"""
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("""
            ModernCard {
                background-color: #242732;
                border: 1px solid #3a3d4a;
                border-radius: 12px;
                margin: 4px;
            }
            ModernCard:hover {
                border: 1px solid #4a9eff;
                background-color: #2a2d3a;
            }
            ModernCard QLabel {
                background: transparent;
                border: none;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 16, 20, 20)
        self.layout.setSpacing(12)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 4px;
                    margin-top: 2px;
                    border: none;
                    background: transparent;
                    padding: 0px;
                }
            """)
            self.layout.addWidget(title_label)

class ModernButton(QPushButton):
    """Modern button with hover effects and gradients"""
    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setMinimumHeight(36)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        
        if button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a9eff, stop:1 #357abd);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5aa7ff, stop:1 #4287d6);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3a8eef, stop:1 #2a6bad);
                }
            """)
        elif button_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3a3d4a, stop:1 #2a2d3a);
                    color: #e1e5e9;
                    border: 1px solid #4a4d5a;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a4d5a, stop:1 #3a3d4a);
                    border: 1px solid #5a5d6a;
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2a2d3a, stop:1 #1a1d2a);
                }
            """)
        elif button_type == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ff6b6b, stop:1 #ee5a5a);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ff7b7b, stop:1 #ff6a6a);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ef5b5b, stop:1 #de4a4a);
                }
            """)

class TextAnonymizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Anonymization Tool - 2025 Edition")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Current configuration
        self.current_config = {
            "config_name": "Default",
            "replacements": [],
            "case_insensitive": False,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "last_modified": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Original text storage for de-anonymization
        self.original_text = ""
        
        self.init_ui()
        self.load_config_list()
        
    def apply_dark_theme(self):
        """Apply comprehensive dark theme to the application"""
        # Set palette for more reliable cross-platform dark theme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(26, 29, 35))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(225, 229, 233))
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 33, 38))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(42, 45, 58))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(26, 29, 35))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(225, 229, 233))
        palette.setColor(QPalette.ColorRole.Text, QColor(225, 229, 233))
        palette.setColor(QPalette.ColorRole.Button, QColor(42, 45, 58))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(225, 229, 233))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(74, 158, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 158, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)
        
        # Ensure background is painted
        self.setAutoFillBackground(True)
        
        # Set the main window background color directly
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1d23;
                color: #e1e5e9;
            }
            
            QWidget {
                background-color: #1a1d23;
                color: #e1e5e9;
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            }
            
            QLabel {
                color: #e1e5e9;
                font-size: 13px;
                font-weight: 500;
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2d3a, stop:1 #232530);
                border: 1px solid #3a3d4a;
                border-radius: 8px;
                padding: 8px 12px;
                color: #e1e5e9;
                font-size: 13px;
                min-height: 20px;
                selection-background-color: #4a9eff;
            }
            QLineEdit:focus {
                border: 2px solid #4a9eff;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d3140, stop:1 #252835);
            }
            
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e2126, stop:1 #181b20);
                border: 1px solid #2a2d3a;
                border-radius: 10px;
                color: #e1e5e9;
                font-family: 'Monaco', 'Menlo', 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                padding: 12px;
                selection-background-color: #4a9eff;
                selection-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #4a9eff;
            }
            
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2d3a, stop:1 #232530);
                border: 1px solid #3a3d4a;
                border-radius: 8px;
                padding: 8px 12px;
                color: #e1e5e9;
                font-size: 13px;
                min-height: 20px;
            }
            QComboBox:hover {
                border: 1px solid #4a4d5a;
            }
            QComboBox:focus {
                border: 2px solid #4a9eff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #6a6d7a;
                width: 6px;
                height: 6px;
                border-top: none;
                border-right: none;
                transform: rotate(45deg);
                margin-right: 8px;
            }
            /* Fix for macOS dropdown styling */
            QComboBox::item {
                background-color: #2a2d3a;
                color: #e1e5e9;
            }
            QComboBox::item:selected {
                background-color: #4a9eff;
                color: white;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2d3a;
                border: 1px solid #3a3d4a;
                color: #e1e5e9;
                selection-background-color: #4a9eff;
            }
            
            QTableWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e2126, stop:1 #181b20);
                border: 1px solid #2a2d3a;
                border-radius: 10px;
                color: #e1e5e9;
                gridline-color: #3a3d4a;
                font-size: 13px;
                selection-background-color: #4a9eff;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
                border-bottom: 1px solid #2a2d3a;
            }
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a9eff, stop:1 #357abd);
                color: white;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2d3a, stop:1 #232530);
                color: #e1e5e9;
                border: none;
                border-bottom: 2px solid #3a3d4a;
                padding: 6px;
                font-weight: 600;
                font-size: 12px;
                max-height: 32px;
            }
            
            QCheckBox {
                color: #e1e5e9;
                font-size: 13px;
                spacing: 8px;
            }
            /* unchecked */
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #4a4d5a;
                border-radius: 4px;
                background: #232530;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #5a5d6a;
            }
            /* checked */
            QCheckBox::indicator:checked {
                background: #4caf50;
                border: 2px solid #4caf50;
            }
            
            QSplitter::handle {
                background: #2a2d3a;
                width: 1px;
                height: 1px;
            }
            QSplitter::handle:hover {
                background: #4a9eff;
            }
            
            QScrollBar:vertical {
                background: #1a1d23;
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #3a3d4a;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4a4d5a;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QMessageBox {
                background: #2a2d3a;
                color: #e1e5e9;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a9eff, stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                margin: 2px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5aa7ff, stop:1 #4287d6);
            }
        """)
        
    def init_ui(self):
        # Central widget with modern styling
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #1a1d23;")
        self.setCentralWidget(central_widget)
        
        # Main layout with proper spacing
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left Panel - Text Input/Output
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right Panel - Configuration Management
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial splitter proportions
        splitter.setSizes([900, 500])
        
    def create_left_panel(self):
        # Left panel with modern card design
        left_card = ModernCard("Text Processing")
        
        # Text area with improved styling
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Enter your text here to anonymize or de-anonymize...")
        self.text_area.setMinimumHeight(500)
        
        left_card.layout.addWidget(self.text_area)
        
        # Action buttons with modern styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.anonymize_btn = ModernButton("🔒 Anonymize", "primary")
        self.anonymize_btn.clicked.connect(self.anonymize_text)
        button_layout.addWidget(self.anonymize_btn)
        
        self.deanonymize_btn = ModernButton("🔓 De-anonymize", "secondary")
        self.deanonymize_btn.clicked.connect(self.deanonymize_text)
        button_layout.addWidget(self.deanonymize_btn)
        
        self.clear_btn = ModernButton("🗑️ Clear", "secondary")
        self.clear_btn.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_btn)
        
        self.copy_btn = ModernButton("📋 Copy", "secondary")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_btn)
        
        button_layout.addStretch()
        left_card.layout.addLayout(button_layout)
        
        return left_card
        
    def create_right_panel(self):
        # Right panel container
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(16)
        
        # Configuration selector card
        config_card = ModernCard("Configuration")
        
        config_label = QLabel("Active Configuration:")
        config_label.setStyleSheet("background: transparent; border: none;")
        config_card.layout.addWidget(config_label)
        
        self.config_combo = QComboBox()
        self.config_combo.currentTextChanged.connect(self.on_config_selected)
        config_card.layout.addWidget(self.config_combo)
        
        name_label = QLabel("Configuration Name:")
        name_label.setStyleSheet("background: transparent; border: none;")
        config_card.layout.addWidget(name_label)
        
        self.config_name_entry = QLineEdit("Default")
        config_card.layout.addWidget(self.config_name_entry)
        
        # Case mode combo (Case sensitive / Case insensitive)
        self.case_mode_combo = QComboBox()
        self.case_mode_combo.addItems(["Case sensitive", "Case insensitive"])
        self.case_mode_combo.setToolTip("Choose how replacements handle letter casing")
        config_card.layout.addWidget(self.case_mode_combo)
        
        right_layout.addWidget(config_card)
        
        # Replacement rules card
        rules_card = ModernCard("Replacement Rules")
        
        # Create a frame for the table to contain it properly
        table_frame = QFrame()
        table_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        table_frame.setStyleSheet("""
            QFrame {
                background-color: #1e2126;
                border: 1px solid #2a2d3a;
                border-radius: 8px;
                margin: 0px;
                padding: 0px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)
        
        # Rules table inside the frame
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(2)
        self.rules_table.setHorizontalHeaderLabels(["Original", "Replacement"])
        self.rules_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.rules_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.rules_table.itemSelectionChanged.connect(self.on_rule_selected)
        # Set a minimum height to show more rows
        self.rules_table.setMinimumHeight(150)
        # Allow table to expand/shrink vertically as needed within layout
        self.rules_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Enable proper scrolling
        self.rules_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.rules_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.rules_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e2126;
                border: none;
                border-radius: 8px;
            }
        """)
        table_layout.addWidget(self.rules_table)
        rules_card.layout.addWidget(table_frame, 2)  # increased stretch factor from 1 to 2
        
        # Add clear separation - reduced from 20 to 5
        rules_card.layout.addSpacing(5)
        
        # Rule editing section
        edit_frame = QFrame()
        edit_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
                margin-top: 5px;
            }
        """)
        edit_layout = QVBoxLayout(edit_frame)
        # Keep input section height fixed so table gets extra space
        edit_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        edit_frame.setMaximumHeight(180)
        edit_layout.setContentsMargins(0, 5, 0, 0)
        edit_layout.setSpacing(8)
        
        # Rule input fields
        rule_edit_layout = QGridLayout()
        rule_edit_layout.setSpacing(8)
        rule_edit_layout.setContentsMargins(0, 0, 0, 0)
        
        rule_edit_layout.addWidget(QLabel("Original:"), 0, 0)
        self.original_entry = QLineEdit()
        self.original_entry.setPlaceholderText("Text to replace...")
        rule_edit_layout.addWidget(self.original_entry, 0, 1)
        
        rule_edit_layout.addWidget(QLabel("Replacement:"), 1, 0)
        self.replacement_entry = QLineEdit()
        self.replacement_entry.setPlaceholderText("Replacement text...")
        rule_edit_layout.addWidget(self.replacement_entry, 1, 1)
        
        edit_layout.addLayout(rule_edit_layout)
        
        # Rule management buttons
        rule_buttons_layout = QHBoxLayout()
        rule_buttons_layout.setSpacing(8)
        rule_buttons_layout.setContentsMargins(0, 10, 0, 0)
        
        self.add_rule_btn = ModernButton("➕ Add", "primary")
        self.add_rule_btn.clicked.connect(self.add_rule)
        rule_buttons_layout.addWidget(self.add_rule_btn)
        
        self.update_rule_btn = ModernButton("✏️ Update", "secondary")
        self.update_rule_btn.clicked.connect(self.update_rule)
        rule_buttons_layout.addWidget(self.update_rule_btn)
        
        self.remove_rule_btn = ModernButton("🗑️ Remove", "danger")
        self.remove_rule_btn.clicked.connect(self.remove_rule)
        rule_buttons_layout.addWidget(self.remove_rule_btn)
        
        edit_layout.addLayout(rule_buttons_layout)
        rules_card.layout.addWidget(edit_frame, 0)
        right_layout.addWidget(rules_card)
        
        # Configuration management card
        mgmt_card = ModernCard("Configuration Management")
        
        config_buttons_layout = QGridLayout()
        config_buttons_layout.setSpacing(8)
        
        self.new_config_btn = ModernButton("📄 New", "secondary")
        self.new_config_btn.clicked.connect(self.new_config)
        config_buttons_layout.addWidget(self.new_config_btn, 0, 0)
        
        self.load_config_btn = ModernButton("📁 Load", "secondary")
        self.load_config_btn.clicked.connect(self.load_config)
        config_buttons_layout.addWidget(self.load_config_btn, 0, 1)
        
        self.save_config_btn = ModernButton("💾 Save", "primary")
        self.save_config_btn.clicked.connect(self.save_config)
        config_buttons_layout.addWidget(self.save_config_btn, 1, 0)
        
        self.delete_config_btn = ModernButton("🗑️ Delete", "danger")
        self.delete_config_btn.clicked.connect(self.delete_config)
        config_buttons_layout.addWidget(self.delete_config_btn, 1, 1)
        
        mgmt_card.layout.addLayout(config_buttons_layout)
        right_layout.addWidget(mgmt_card)
        
        # Add stretch to push everything up
        right_layout.addStretch()
        
        return right_widget
        
    def preserve_case_pattern(self, original_match, replacement):
        """Preserve the case pattern of the original match in the replacement"""
        if len(original_match) == 0:
            return replacement
            
        # If replacement is shorter than original, just use replacement as-is
        if len(replacement) < len(original_match):
            # Apply case pattern to available characters
            result = ""
            for i, char in enumerate(replacement):
                if i < len(original_match):
                    if original_match[i].isupper():
                        result += char.upper()
                    else:
                        result += char.lower()
                else:
                    result += char
            return result
        
        # If replacement is longer or equal, apply pattern and keep extra chars as lowercase
        result = ""
        for i, char in enumerate(replacement):
            if i < len(original_match):
                if original_match[i].isupper():
                    result += char.upper()
                else:
                    result += char.lower()
            else:
                result += char.lower()
        return result
        
    def load_config_list(self):
        """Load all available configuration files"""
        config_files = glob.glob(os.path.join(CONFIGS_DIR, "config_*.json"))
        config_names = [os.path.basename(f).replace("config_", "").replace(".json", "") for f in config_files]
        
        self.config_combo.clear()
        self.config_combo.addItems(config_names)
        
        if config_names:
            self.config_combo.setCurrentText(config_names[0])
            self.on_config_selected(config_names[0])
            
    def on_config_selected(self, config_name):
        """Handle configuration selection"""
        if config_name:
            self.load_config_by_name(config_name)
            
    def load_config_by_name(self, config_name):
        """Load configuration by name"""
        filename = os.path.join(CONFIGS_DIR, f"config_{config_name}.json")
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    self.current_config = json.load(f)
                    self.config_name_entry.setText(self.current_config['config_name'])
                    
                    # Handle case insensitive option (backward compatibility)
                    case_insensitive = self.current_config.get('case_insensitive', False)
                    self.case_mode_combo.setCurrentIndex(1 if case_insensitive else 0)
                    
                    self.refresh_rules_table()
            except Exception as e:
                self.show_error(f"Failed to load configuration: {str(e)}")
                
    def refresh_rules_table(self):
        """Refresh the rules table"""
        self.rules_table.setRowCount(0)
        
        replacements = self.current_config.get('replacements', [])
        self.rules_table.setRowCount(len(replacements))
        
        for idx, rule in enumerate(replacements):
            self.rules_table.setItem(idx, 0, QTableWidgetItem(rule['original']))
            self.rules_table.setItem(idx, 1, QTableWidgetItem(rule['replacement']))
        
        # Ensure table updates and scrollbars are visible if needed
        self.rules_table.resizeRowsToContents()
        self.rules_table.scrollToTop()
            
    def on_rule_selected(self):
        """Handle rule selection in table"""
        current_row = self.rules_table.currentRow()
        if current_row >= 0:
            original_item = self.rules_table.item(current_row, 0)
            replacement_item = self.rules_table.item(current_row, 1)
            
            if original_item and replacement_item:
                self.original_entry.setText(original_item.text())
                self.replacement_entry.setText(replacement_item.text())
                
    def add_rule(self):
        """Add a new replacement rule"""
        original = self.original_entry.text().strip()
        replacement = self.replacement_entry.text().strip()
        
        if not original or not replacement:
            self.show_warning("Both original and replacement text are required.")
            return
            
        # Check for duplicates
        for rule in self.current_config['replacements']:
            if rule['original'] == original:
                self.show_warning("Rule with this original text already exists.")
                return
                
        # Add the rule
        self.current_config['replacements'].append({
            'original': original,
            'replacement': replacement
        })
        
        self.current_config['last_modified'] = datetime.now().strftime("%Y-%m-%d")
        self.refresh_rules_table()
        
        # Clear entry fields
        self.original_entry.clear()
        self.replacement_entry.clear()
        
    def remove_rule(self):
        """Remove selected rule"""
        current_row = self.rules_table.currentRow()
        if current_row < 0:
            self.show_warning("Please select a rule to remove.")
            return
            
        original_item = self.rules_table.item(current_row, 0)
        if original_item:
            original_text = original_item.text()
            
            # Remove from config
            self.current_config['replacements'] = [
                rule for rule in self.current_config['replacements']
                if rule['original'] != original_text
            ]
            
            self.current_config['last_modified'] = datetime.now().strftime("%Y-%m-%d")
            self.refresh_rules_table()
            
            # Clear entry fields
            self.original_entry.clear()
            self.replacement_entry.clear()
            
    def update_rule(self):
        """Update selected rule"""
        current_row = self.rules_table.currentRow()
        if current_row < 0:
            self.show_warning("Please select a rule to update.")
            return
            
        original_item = self.rules_table.item(current_row, 0)
        if not original_item:
            return
            
        old_original = original_item.text()
        new_original = self.original_entry.text().strip()
        new_replacement = self.replacement_entry.text().strip()
        
        if not new_original or not new_replacement:
            self.show_warning("Both original and replacement text are required.")
            return
            
        # Check for duplicates (excluding current rule)
        for rule in self.current_config['replacements']:
            if rule['original'] == new_original and rule['original'] != old_original:
                self.show_warning("Rule with this original text already exists.")
                return
                
        # Update the rule
        for rule in self.current_config['replacements']:
            if rule['original'] == old_original:
                rule['original'] = new_original
                rule['replacement'] = new_replacement
                break
                
        self.current_config['last_modified'] = datetime.now().strftime("%Y-%m-%d")
        self.refresh_rules_table()
        
    def new_config(self):
        """Create a new configuration"""
        self.current_config = {
            "config_name": "New_Config",
            "replacements": [],
            "case_insensitive": False,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "last_modified": datetime.now().strftime("%Y-%m-%d")
        }
        self.config_name_entry.setText("New_Config")
        self.case_mode_combo.setCurrentIndex(0) # Default to case sensitive
        self.refresh_rules_table()
        
    def load_config(self):
        """Load configuration from file in the 'configs' folder"""
        configs_dir = os.path.join(os.getcwd(), "configs")
        if not os.path.isdir(configs_dir):
            os.makedirs(configs_dir, exist_ok=True)

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Configuration",
            configs_dir,
            "JSON files (*.json)"
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.current_config = json.load(f)
                    self.config_name_entry.setText(self.current_config['config_name'])

                    case_insensitive = self.current_config.get('case_insensitive', False)
                    self.case_mode_combo.setCurrentIndex(1 if case_insensitive else 0)

                    self.refresh_rules_table()
                    self.load_config_list()
            except Exception as e:
                self.show_error(f"Failed to load configuration: {str(e)}")
                    
    def save_config(self):
        """Save current configuration to file"""
        config_name = self.config_name_entry.text().strip()
        if not config_name:
            self.show_warning("Please enter a configuration name.")
            return
            
        self.current_config['config_name'] = config_name
        self.current_config['case_insensitive'] = (self.case_mode_combo.currentIndex() == 1)
        self.current_config['last_modified'] = datetime.now().strftime("%Y-%m-%d")
        
        filename = os.path.join(CONFIGS_DIR, f"config_{config_name}.json")
        try:
            with open(filename, 'w') as f:
                json.dump(self.current_config, f, indent=2)
            self.show_success(f"Configuration saved successfully!")
            self.load_config_list()
        except Exception as e:
            self.show_error(f"Failed to save configuration: {str(e)}")
            
    def delete_config(self):
        """Delete selected configuration"""
        selected_config = self.config_combo.currentText()
        if not selected_config:
            self.show_warning("Please select a configuration to delete.")
            return
            
        reply = QMessageBox.question(
            self, "Confirm Deletion", 
            f"Are you sure you want to delete configuration '{selected_config}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            filename = os.path.join(CONFIGS_DIR, f"config_{selected_config}.json")
            try:
                os.remove(filename)
                self.show_success(f"Configuration '{selected_config}' deleted successfully!")
                self.load_config_list()
            except Exception as e:
                self.show_error(f"Failed to delete configuration: {str(e)}")
                
    def anonymize_text(self):
        """Anonymize text using current configuration"""
        text = self.text_area.toPlainText()
        if not text:
            self.show_warning("Please enter text to anonymize.")
            return
            
        # Store original text for de-anonymization
        self.original_text = text
        
        # Apply replacements
        anonymized_text = text
        case_insensitive = (self.case_mode_combo.currentIndex() == 1)
        
        for rule in self.current_config['replacements']:
            original = rule['original']
            replacement = rule['replacement']
            
            if case_insensitive:
                # Use regex for case-insensitive replacement with case preservation
                def replace_func(match):
                    matched_text = match.group(0)
                    return self.preserve_case_pattern(matched_text, replacement)
                
                # Create regex pattern that matches whole words to avoid partial matches
                pattern = r'\b' + re.escape(original) + r'\b'
                anonymized_text = re.sub(pattern, replace_func, anonymized_text, flags=re.IGNORECASE)
            else:
                # Standard case-sensitive replacement
                anonymized_text = anonymized_text.replace(original, replacement)
            
        # Update text area
        self.text_area.setPlainText(anonymized_text)
        self.show_success("Text anonymized successfully! 🔒")
        
    def deanonymize_text(self):
        """De-anonymize text using current configuration"""
        text = self.text_area.toPlainText()
        if not text:
            self.show_warning("Please enter text to de-anonymize.")
            return
            
        # Apply reverse replacements
        deanonymized_text = text
        case_insensitive = (self.case_mode_combo.currentIndex() == 1)
        
        for rule in reversed(self.current_config['replacements']):
            original = rule['original']
            replacement = rule['replacement']
            
            if case_insensitive:
                # Use regex for case-insensitive replacement with case preservation
                def replace_func(match):
                    matched_text = match.group(0)
                    return self.preserve_case_pattern(matched_text, original)
                
                # Create regex pattern that matches whole words to avoid partial matches
                pattern = r'\b' + re.escape(replacement) + r'\b'
                deanonymized_text = re.sub(pattern, replace_func, deanonymized_text, flags=re.IGNORECASE)
            else:
                # Standard case-sensitive replacement
                deanonymized_text = deanonymized_text.replace(replacement, original)
            
        # Update text area
        self.text_area.setPlainText(deanonymized_text)
        self.show_success("Text de-anonymized successfully! 🔓")
        
    def clear_text(self):
        """Clear the text area"""
        self.text_area.clear()
        
    def copy_to_clipboard(self):
        """Copy text area content to clipboard"""
        text = self.text_area.toPlainText()
        if text:
            try:
                pyperclip.copy(text)
                self.show_success("Text copied to clipboard! 📋")
            except Exception as e:
                self.show_error(f"Failed to copy to clipboard: {str(e)}")
        else:
            self.show_warning("No text to copy.")
    
    def show_success(self, message):
        """Show success message with modern styling"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Success")
        msg.setText(message)
        msg.exec()
    
    def show_warning(self, message):
        """Show warning message with modern styling"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Warning")
        msg.setText(message)
        msg.exec()
    
    def show_error(self, message):
        """Show error message with modern styling"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec()


def main():
    app = QApplication(sys.argv)
    
    # Set application properties for better styling
    app.setApplicationName("Text Anonymizer")
    app.setApplicationVersion("2025.1")
    
    # Apply custom style for macOS to fix dropdown styling
    if sys.platform == "darwin":
        app.setStyle(DarkProxyStyle())
    
    window = TextAnonymizer()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 