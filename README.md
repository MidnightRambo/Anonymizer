# Text Anonymization/De-anonymization Tool

A Python-based desktop application with GUI that enables users to anonymize sensitive data in text (code, emails, SQL statements, etc.) before sharing with LLMs, and then de-anonymize the LLM responses.

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

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd text-anonymizer
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

Configurations are stored as JSON files with the following structure:

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

### Example Use Cases

#### Code Anonymization

**Original Code:**
```python
def connect_to_database():
    conn = psycopg2.connect(
        host="prod-server.company.com",
        database="customer_data",
        user="admin_user",
        password="secret123"
    )
    return conn
```

**Anonymized Code:**
```python
def connect_to_database():
    conn = psycopg2.connect(
        host="generic-server.example.com",
        database="sample_data",
        user="db_user",
        password="PASSWORD_HIDDEN"
    )
    return conn
```

#### SQL Query Anonymization

**Original:**
```sql
SELECT customer_id, email, phone 
FROM production_customers 
WHERE company_name = 'Acme Corp';
```

**Anonymized:**
```sql
SELECT customer_id, email, phone 
FROM sample_customers 
WHERE company_name = 'COMPANY_ANONYMOUS';
```

#### Email Anonymization

**Original:**
```
From: john.smith@acmecorp.com
To: api-support@thirdparty.com
Subject: API Integration Issue

Hi,

We're having trouble with the API endpoint at https://api.acmecorp.com/v1/customers.
The API key abc123def456 doesn't seem to be working.
```

**Anonymized:**
```
From: user1@example.com
To: api-support@thirdparty.com
Subject: API Integration Issue

Hi,

We're having trouble with the API endpoint at https://api.example.com/v1/customers.
The API key API_KEY_HIDDEN doesn't seem to be working.
```

#### Case-Insensitive Replacement Example

**Original:**
```
David works at Microsoft headquarters.
DAVID also uses MICROSOFT Azure services.
david prefers microsoft products.
DaViD attended the MiCrOsOfT conference.
```

**Anonymized (with case-insensitive enabled):**
```
Lucas works at TECH_COMPANY headquarters.
LUCAS also uses TECH_COMPANY Azure services.
lucas prefers TECH_COMPANY products.
LuCaS attended the TECH_COMPANY conference.
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
   - Verify the file is in the same directory as main.py

2. **Clipboard Not Working**
   - Ensure pyperclip is installed: `pip install pyperclip`
   - On Linux, you may need to install xclip: `sudo apt-get install xclip`

3. **Text Formatting Issues**
   - The tool preserves all formatting (spaces, tabs, line breaks)
   - If formatting appears wrong, check your original text

### Error Messages

- **"Both original and replacement text are required"**: Fill in both fields when adding rules
- **"Rule with this original text already exists"**: Each original text must be unique
- **"Please select a rule to remove/update"**: Click on a rule in the table first

## File Structure

```
text-anonymizer/
├── main.py                  # Main application file
├── requirements.txt         # Python dependencies
├── config_Sample.json       # Sample configuration file
├── README.md               # This file
└── venv/                   # Virtual environment (created during setup)
```

## Dependencies

- **PyQt6**: Modern GUI framework for cross-platform applications
- **pyperclip**: For clipboard operations
- **json**: JSON handling (built into Python)
- **glob**: File pattern matching (built into Python)
- **datetime**: Date/time handling (built into Python)

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues, questions, or feature requests, please:
1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed information 