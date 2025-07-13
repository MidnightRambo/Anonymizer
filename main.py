import sys
import json
import os
import glob
import re
from datetime import datetime
import pyperclip
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                            QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
                            QComboBox, QMessageBox, QFileDialog, QSplitter,
                            QGroupBox, QHeaderView, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class TextAnonymizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Anonymization/De-anonymization Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        
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
        
    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left Panel - Text Input/Output
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right Panel - Configuration Management
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial splitter proportions
        splitter.setSizes([800, 400])
        
    def create_left_panel(self):
        # Left panel group box
        left_group = QGroupBox("Text Input/Output")
        left_layout = QVBoxLayout(left_group)
        
        # Text area with improved formatting
        self.text_area = QTextEdit()
        # Use a monospace font that's available on macOS
        self.text_area.setFont(QFont("Monaco", 11))  # Monaco is available on macOS
        self.text_area.setMinimumHeight(400)
        
        # Improve text area properties for better formatting
        self.text_area.setAcceptRichText(False)  # Only plain text
        self.text_area.setWordWrapMode(0)  # No word wrapping
        self.text_area.setTabStopWidth(40)  # Set tab width
        
        # Set style for better formatting preservation (system theme compatible)
        self.text_area.setStyleSheet("""
            QTextEdit {
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 8px;
                font-family: Monaco, 'Courier New', monospace;
                selection-background-color: palette(highlight);
                selection-color: palette(highlighted-text);
            }
        """)
        
        left_layout.addWidget(self.text_area)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Control buttons
        self.anonymize_btn = QPushButton("Anonymize")
        self.anonymize_btn.clicked.connect(self.anonymize_text)
        button_layout.addWidget(self.anonymize_btn)
        
        self.deanonymize_btn = QPushButton("De-anonymize")
        self.deanonymize_btn.clicked.connect(self.deanonymize_text)
        button_layout.addWidget(self.deanonymize_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_btn)
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_btn)
        
        button_layout.addStretch()
        left_layout.addLayout(button_layout)
        
        return left_group
        
    def create_right_panel(self):
        # Right panel group box
        right_group = QGroupBox("Configuration Management")
        right_layout = QVBoxLayout(right_group)
        
        # Configuration selector
        config_layout = QVBoxLayout()
        config_layout.addWidget(QLabel("Configuration:"))
        
        self.config_combo = QComboBox()
        self.config_combo.currentTextChanged.connect(self.on_config_selected)
        config_layout.addWidget(self.config_combo)
        
        # Configuration name
        config_layout.addWidget(QLabel("Configuration Name:"))
        self.config_name_entry = QLineEdit("Default")
        config_layout.addWidget(self.config_name_entry)
        
        # Case insensitive option
        self.case_insensitive_checkbox = QCheckBox("Case insensitive replacement")
        self.case_insensitive_checkbox.setToolTip("When enabled, 'David' will match 'david', 'DAVID', etc. and preserve the case pattern")
        config_layout.addWidget(self.case_insensitive_checkbox)
        
        right_layout.addLayout(config_layout)
        
        # Replacement rules section
        rules_group = QGroupBox("Replacement Rules")
        rules_layout = QVBoxLayout(rules_group)
        
        # Rules table
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(2)
        self.rules_table.setHorizontalHeaderLabels(["Original", "Replacement"])
        self.rules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rules_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.rules_table.itemSelectionChanged.connect(self.on_rule_selected)
        rules_layout.addWidget(self.rules_table)
        
        # Rule editing
        rule_edit_layout = QGridLayout()
        rule_edit_layout.addWidget(QLabel("Original:"), 0, 0)
        self.original_entry = QLineEdit()
        rule_edit_layout.addWidget(self.original_entry, 0, 1)
        
        rule_edit_layout.addWidget(QLabel("Replacement:"), 1, 0)
        self.replacement_entry = QLineEdit()
        rule_edit_layout.addWidget(self.replacement_entry, 1, 1)
        
        rules_layout.addLayout(rule_edit_layout)
        
        # Rule buttons
        rule_buttons_layout = QHBoxLayout()
        
        self.add_rule_btn = QPushButton("Add Rule")
        self.add_rule_btn.clicked.connect(self.add_rule)
        rule_buttons_layout.addWidget(self.add_rule_btn)
        
        self.remove_rule_btn = QPushButton("Remove Rule")
        self.remove_rule_btn.clicked.connect(self.remove_rule)
        rule_buttons_layout.addWidget(self.remove_rule_btn)
        
        self.update_rule_btn = QPushButton("Update Rule")
        self.update_rule_btn.clicked.connect(self.update_rule)
        rule_buttons_layout.addWidget(self.update_rule_btn)
        
        rules_layout.addLayout(rule_buttons_layout)
        right_layout.addWidget(rules_group)
        
        # Configuration buttons
        config_buttons_layout = QGridLayout()
        
        self.new_config_btn = QPushButton("New Config")
        self.new_config_btn.clicked.connect(self.new_config)
        config_buttons_layout.addWidget(self.new_config_btn, 0, 0)
        
        self.load_config_btn = QPushButton("Load Config")
        self.load_config_btn.clicked.connect(self.load_config)
        config_buttons_layout.addWidget(self.load_config_btn, 0, 1)
        
        self.save_config_btn = QPushButton("Save Config")
        self.save_config_btn.clicked.connect(self.save_config)
        config_buttons_layout.addWidget(self.save_config_btn, 1, 0)
        
        self.delete_config_btn = QPushButton("Delete Config")
        self.delete_config_btn.clicked.connect(self.delete_config)
        config_buttons_layout.addWidget(self.delete_config_btn, 1, 1)
        
        right_layout.addLayout(config_buttons_layout)
        
        return right_group
        
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
        config_files = glob.glob("config_*.json")
        config_names = [f.replace("config_", "").replace(".json", "") for f in config_files]
        
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
        filename = f"config_{config_name}.json"
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    self.current_config = json.load(f)
                    self.config_name_entry.setText(self.current_config['config_name'])
                    
                    # Handle case insensitive option (backward compatibility)
                    case_insensitive = self.current_config.get('case_insensitive', False)
                    self.case_insensitive_checkbox.setChecked(case_insensitive)
                    
                    self.refresh_rules_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")
                
    def refresh_rules_table(self):
        """Refresh the rules table"""
        self.rules_table.setRowCount(0)
        
        for rule in self.current_config.get('replacements', []):
            row = self.rules_table.rowCount()
            self.rules_table.insertRow(row)
            self.rules_table.setItem(row, 0, QTableWidgetItem(rule['original']))
            self.rules_table.setItem(row, 1, QTableWidgetItem(rule['replacement']))
            
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
            QMessageBox.warning(self, "Warning", "Both original and replacement text are required.")
            return
            
        # Check for duplicates
        for rule in self.current_config['replacements']:
            if rule['original'] == original:
                QMessageBox.warning(self, "Warning", "Rule with this original text already exists.")
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
            QMessageBox.warning(self, "Warning", "Please select a rule to remove.")
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
            QMessageBox.warning(self, "Warning", "Please select a rule to update.")
            return
            
        original_item = self.rules_table.item(current_row, 0)
        if not original_item:
            return
            
        old_original = original_item.text()
        new_original = self.original_entry.text().strip()
        new_replacement = self.replacement_entry.text().strip()
        
        if not new_original or not new_replacement:
            QMessageBox.warning(self, "Warning", "Both original and replacement text are required.")
            return
            
        # Check for duplicates (excluding current rule)
        for rule in self.current_config['replacements']:
            if rule['original'] == new_original and rule['original'] != old_original:
                QMessageBox.warning(self, "Warning", "Rule with this original text already exists.")
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
        self.case_insensitive_checkbox.setChecked(False)
        self.refresh_rules_table()
        
    def load_config(self):
        """Load configuration from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON files (*.json)"
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.current_config = json.load(f)
                    self.config_name_entry.setText(self.current_config['config_name'])
                    
                    # Handle case insensitive option (backward compatibility)
                    case_insensitive = self.current_config.get('case_insensitive', False)
                    self.case_insensitive_checkbox.setChecked(case_insensitive)
                    
                    self.refresh_rules_table()
                    self.load_config_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")
                
    def save_config(self):
        """Save current configuration to file"""
        config_name = self.config_name_entry.text().strip()
        if not config_name:
            QMessageBox.warning(self, "Warning", "Please enter a configuration name.")
            return
            
        self.current_config['config_name'] = config_name
        self.current_config['case_insensitive'] = self.case_insensitive_checkbox.isChecked()
        self.current_config['last_modified'] = datetime.now().strftime("%Y-%m-%d")
        
        filename = f"config_{config_name}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(self.current_config, f, indent=2)
            QMessageBox.information(self, "Success", f"Configuration saved as {filename}")
            self.load_config_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")
            
    def delete_config(self):
        """Delete selected configuration"""
        selected_config = self.config_combo.currentText()
        if not selected_config:
            QMessageBox.warning(self, "Warning", "Please select a configuration to delete.")
            return
            
        reply = QMessageBox.question(
            self, "Confirm", 
            f"Are you sure you want to delete configuration '{selected_config}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            filename = f"config_{selected_config}.json"
            try:
                os.remove(filename)
                QMessageBox.information(self, "Success", f"Configuration '{selected_config}' deleted.")
                self.load_config_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete configuration: {str(e)}")
                
    def anonymize_text(self):
        """Anonymize text using current configuration"""
        text = self.text_area.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to anonymize.")
            return
            
        # Store original text for de-anonymization
        self.original_text = text
        
        # Apply replacements
        anonymized_text = text
        case_insensitive = self.case_insensitive_checkbox.isChecked()
        
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
        
        QMessageBox.information(self, "Success", "Text anonymized successfully.")
        
    def deanonymize_text(self):
        """De-anonymize text using current configuration"""
        text = self.text_area.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to de-anonymize.")
            return
            
        # Apply reverse replacements
        deanonymized_text = text
        case_insensitive = self.case_insensitive_checkbox.isChecked()
        
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
        
        QMessageBox.information(self, "Success", "Text de-anonymized successfully.")
        
    def clear_text(self):
        """Clear the text area"""
        self.text_area.clear()
        
    def copy_to_clipboard(self):
        """Copy text area content to clipboard"""
        text = self.text_area.toPlainText()
        if text:
            try:
                pyperclip.copy(text)
                QMessageBox.information(self, "Success", "Text copied to clipboard.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to copy to clipboard: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No text to copy.")


def main():
    app = QApplication(sys.argv)
    window = TextAnonymizer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 