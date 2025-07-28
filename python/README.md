# Text Anonymizer - Python Version

> **⚠️ Notice**: This is the **legacy Python version**. For the best experience, please use the [**Tauri version**](../tauri/) which has active development and better performance.

A Python-based desktop application with GUI that enables users to anonymize sensitive data in text before sharing with LLMs, and then de-anonymize the LLM responses.

## Features

- **Intuitive GUI**: Clean, user-friendly interface built with PyQt6
- **Text Processing**: Preserve formatting while anonymizing/de-anonymizing text
- **Case-Insensitive Matching**: Optional case-insensitive replacement with case pattern preservation
- **Word-Boundary Control**: Choose whether to replace only whole words or also text inside other words
- **Configuration Management**: Save/load multiple anonymization configurations
- **Reversible Operations**: Ensure perfect de-anonymization of processed text
- **Clipboard Integration**: Easy copy/paste functionality
- **Cross-platform**: Works on Windows, Linux, and macOS

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Navigate to the Python version**
   ```bash
   cd python
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Basic Workflow

1. **Launch the application** by running `python main.py`
2. **Enter text** in the left panel text area
3. **Configure replacement rules** in the right panel
4. **Click "Anonymize"** to replace sensitive data
5. **Share the anonymized text** with LLMs or others
6. **Click "De-anonymize"** to restore original sensitive data

### Configuration Management

#### Creating a New Configuration

1. Click "New Config" to create a fresh configuration
2. Enter a name in the "Configuration Name" field
3. Add replacement rules using the "Original" and "Replacement" fields
4. Click "Add Rule" to save each rule
5. Click "Save Config" to persist the configuration

#### Loading Existing Configurations

1. Use the dropdown menu to select an existing configuration
2. Or click "Load Config" to browse for a configuration file
3. The rules will automatically populate in the interface

#### Managing Replacement Rules

- **Add Rule**: Enter original and replacement text, then click "Add Rule"
- **Remove Rule**: Select a rule in the list and click "Remove Rule"
- **Update Rule**: Select a rule, modify the text fields, and click "Update Rule"

#### Case-Insensitive Replacement

Enable the "Case insensitive replacement" checkbox to make replacements work regardless of case while preserving the original case pattern:

- **David** → **Lucas** (if original is "David" and replacement is "Lucas")
- **david** → **lucas** (lowercase preserved)
- **DAVID** → **LUCAS** (uppercase preserved)
- **DaViD** → **LuCaS** (mixed case pattern preserved)

### Configuration File Format

Configurations are stored as JSON files in the `configs/` directory:

```json
{
  "config_name": "Sample",
  "case_insensitive": true,
  "whole_words_only": false,
  "replacements": [
    {
      "original": "CompanyName Inc.",
      "replacement": "COMPANY_ANONYMOUS"
    },
    {
      "original": "john.doe@company.com",
      "replacement": "user1@example.com"
    }
  ],
  "created_date": "2024-01-15",
  "last_modified": "2024-01-15"
}
```

## GUI Components

### Left Panel - Text Input/Output
- **Text Area**: Large, scrollable text field with monospace font
- **Anonymize Button**: Applies current configuration to replace sensitive data
- **De-anonymize Button**: Reverses the replacement process
- **Clear Button**: Clears the text area
- **Copy to Clipboard Button**: Copies current text to clipboard

### Right Panel - Configuration Management
- **Configuration Dropdown**: Select from existing configurations
- **Configuration Name Field**: Name for the current configuration
- **Case Sensitivity Dropdown**: Select case-sensitive or case-insensitive matching (with case preservation)
- **Word Boundaries Dropdown**: Select whole-word replacement only or allow matches inside words
- **Replacement Rules Table**: View and manage replacement rules
- **Rule Editor**: Add/edit individual replacement rules
- **Configuration Buttons**: New, Load, Save, Delete configurations

## Best Practices

1. **Test Your Rules**: Always test anonymization/de-anonymization with sample data
2. **Order Matters**: Rules are applied in order - be careful with overlapping patterns
3. **Case-Insensitive Matching**: Enable case-insensitive replacement when you want to match names regardless of capitalization
4. **Backup Configurations**: Save important configurations to prevent data loss
5. **Use Descriptive Names**: Give configurations clear, descriptive names
6. **Review Before Sharing**: Always review anonymized text before sharing
7. **Formatting Preservation**: The text area preserves tabs, spaces, and code formatting - paste directly from your IDE or documents

## Troubleshooting

### Common Issues

1. **Configuration Not Loading**
   - Check if the JSON file is properly formatted
   - Verify the file is in the `configs/` directory

2. **Clipboard Not Working**
   - Ensure pyperclip is installed: `pip install pyperclip`
   - On Linux, you may need to install xclip: `sudo apt-get install xclip`

3. **Text Formatting Issues**
   - The tool preserves all formatting (spaces, tabs, line breaks)
   - If formatting appears wrong, check your original text

4. **PyQt6 Installation Issues**
   - On some systems, you may need to install system packages:
     - Ubuntu/Debian: `sudo apt-get install python3-pyqt6`
     - Fedora: `sudo dnf install python3-qt6`
     - macOS: Usually works with pip, but may need Xcode command line tools

### Error Messages

- **"Both original and replacement text are required"**: Fill in both fields when adding rules
- **"Rule with this original text already exists"**: Each original text must be unique
- **"Please select a rule to remove/update"**: Click on a rule in the table first

## File Structure

```
python/
├── main.py                  # Main application file
├── requirements.txt         # Python dependencies
├── configs/                 # Configuration files directory
│   └── config_Sample.json   # Sample configuration file
└── README.md               # This file
```

## Dependencies

- **PyQt6**: Modern GUI framework for cross-platform applications
- **pyperclip**: For clipboard operations
- **json**: JSON handling (built into Python)
- **glob**: File pattern matching (built into Python)
- **datetime**: Date/time handling (built into Python)

## Migration to Tauri Version

If you're currently using the Python version and want to migrate to the Tauri version:

1. **Export your configurations**: Copy your configuration files from `configs/` directory
2. **Install the Tauri version**: Follow the [Tauri installation guide](../tauri/README.md)
3. **Import configurations**: Load your configuration files in the new version
4. **Test thoroughly**: Ensure all your rules work as expected

## Contributing

> **Note**: This Python version is in **maintenance mode**. New features are not being added. Please contribute to the [Tauri version](../tauri/) instead.

Bug fixes and security updates for the Python version are still accepted:

1. Fork the repository
2. Create a feature branch
3. Make your changes to files in the `python/` directory only
4. Test thoroughly
5. Submit a pull request with a clear description of the bug being fixed

## License

This project is open source and available under the MIT License. 