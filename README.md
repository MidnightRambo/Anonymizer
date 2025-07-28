# Text Anonymization/De-anonymization Tool

A cross-platform desktop application that enables users to anonymize sensitive data in text (code, emails, SQL statements, etc.) before sharing with LLMs, and then de-anonymize the LLM responses.

## 🚀 Available Versions

This project provides **two implementations**:

### 🦀 **Tauri Version** (Recommended - Active Development)
- **Location**: [`/tauri`](./tauri/) folder
- **Technology**: Rust + TypeScript/React + Tauri
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Status**: ✅ **Active development** - All new features and improvements
- **Performance**: Native performance with modern UI
- **Installation**: Download pre-built binaries from [Releases](../../releases)

### 🐍 **Python Version** (Legacy - Maintenance Only)
- **Location**: [`/python`](./python/) folder  
- **Technology**: Python + PyQt6
- **Platform**: Cross-platform (requires Python runtime)
- **Status**: 🔒 **Maintenance only** - No new features planned
- **Performance**: Good performance, requires Python installation
- **Installation**: Manual setup with Python environment

> **💡 Recommendation**: Use the **Tauri version** for the best experience, performance, and latest features. The Python version is provided for compatibility and legacy use cases.

## 📥 Quick Start (Tauri Version)

### Option 1: Download Pre-built Binaries (Recommended)
1. Go to the [Releases](../../releases) page
2. Download the appropriate file for your OS:
   - **Windows**: `.exe` or `.msi` installer
   - **macOS**: `.dmg` installer
   - **Linux**: `.AppImage` or `.deb` package
3. Install and run the application

### Option 2: Build from Source
```bash
# Clone the repository
git clone <repository-url>
cd text-anonymizer

# Navigate to Tauri version
cd tauri

# Install Node.js dependencies
npm install

# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs/ | sh

# Build and run in development mode
npm run tauri dev

# Or build for production
npm run tauri build
```

## 📥 Python Version Setup

If you prefer the Python version, see the detailed setup instructions in [`/python/README.md`](./python/README.md).

<details>
<summary>Quick Python Setup</summary>

```bash
# Navigate to Python version
cd python

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

</details>

## ✨ Features

- **Intuitive GUI**: Modern, clean interface with excellent UX
- **Text Processing**: Preserve formatting while anonymizing/de-anonymizing text
- **Case-Insensitive Matching**: Optional case-insensitive replacement with case pattern preservation
- **Word-Boundary Control**: Choose whether to replace only whole words or also text inside other words
- **Configuration Management**: Save/load multiple anonymization configurations
- **Reversible Operations**: Ensure perfect de-anonymization of processed text
- **Clipboard Integration**: Easy copy/paste functionality
- **Cross-platform**: Works on Windows, Linux, and macOS
- **High Performance**: Native performance (Tauri) or Python runtime performance

## 🔧 Usage

### Basic Workflow

1. **Launch the application**
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

## 💡 Example Use Cases

### Code Anonymization

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

### SQL Query Anonymization

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

### Email Anonymization

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

## 🏗️ Development & Building

### GitHub Actions

This repository includes automated building via GitHub Actions:

- **Automatic builds** on push to main/master branches
- **Cross-platform compilation** for Windows (.exe) and macOS (.dmg)
- **Release automation** when creating GitHub releases
- **Artifact uploads** for easy access to built binaries

### Manual Building

See the respective README files in each version folder:
- [Tauri Development Guide](./tauri/README.md)
- [Python Development Guide](./python/README.md)

## 📁 Project Structure

```
text-anonymizer/
├── tauri/                   # 🦀 Tauri version (Rust + React)
│   ├── src/                 # React frontend
│   ├── src-tauri/           # Rust backend
│   ├── package.json         # Node.js dependencies
│   └── README.md            # Tauri-specific documentation
├── python/                  # 🐍 Python version (PyQt6)
│   ├── main.py              # Main application file
│   ├── requirements.txt     # Python dependencies
│   ├── configs/             # Sample configurations
│   └── README.md            # Python-specific documentation
├── .github/workflows/       # 🔄 GitHub Actions CI/CD
│   └── build.yml            # Build automation
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes to the **Tauri version** (active development)
4. Test thoroughly on multiple platforms
5. Submit a pull request

> **Note**: New features should be implemented in the Tauri version only. Python version contributions are limited to critical bug fixes.

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues, questions, or feature requests:

1. Check the [Issues](../../issues) page for existing reports
2. Review the troubleshooting sections in version-specific READMEs
3. Create a new issue with:
   - Detailed description
   - Steps to reproduce
   - System information (OS, version)
   - Screenshots (if applicable)

## 🎯 Roadmap

### Tauri Version (Active)
- [ ] Enhanced UI/UX improvements
- [ ] Plugin system for custom anonymization rules
- [ ] Cloud configuration sync
- [ ] Advanced regex pattern support
- [ ] Batch file processing
- [ ] CLI interface

### Python Version (Maintenance Only)
- Critical bug fixes only
- Security updates 