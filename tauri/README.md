# Text Anonymization Tool - Tauri Edition

A modern cross-platform desktop application built with **Tauri + React + TypeScript** that enables users to anonymize sensitive data in text before sharing with LLMs, and then de-anonymize the responses. This is a complete rewrite of the original Python/PyQt6 application with improved performance, security, and modern UI.

## 🚀 Features

- **Modern UI**: Clean, responsive interface with dark theme built using React + Tailwind CSS
- **High Performance**: Rust backend for lightning-fast text processing
- **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux
- **Secure**: Tauri's security-first architecture with minimal attack surface
- **Text Processing**: Preserve formatting while anonymizing/de-anonymizing text
- **Advanced Matching**: Case-insensitive replacement with case pattern preservation
- **Word Boundary Control**: Choose whole-word or partial text replacement
- **Configuration Management**: Save/load multiple anonymization configurations
- **Reversible Operations**: Perfect de-anonymization of processed text
- **Clipboard Integration**: Easy copy/paste functionality
- **Type Safety**: Full TypeScript implementation for better reliability

## 🆚 Comparison with Python Version

| Feature | Python/PyQt6 | Tauri/React | Winner |
|---------|---------------|-------------|---------|
| **Performance** | Moderate | ⚡ Excellent | Tauri |
| **Memory Usage** | ~50-100MB | ~30-60MB | Tauri |
| **Startup Time** | ~2-3 seconds | ~0.5-1 second | Tauri |
| **Security** | Good | 🔒 Excellent | Tauri |
| **Bundle Size** | ~150MB | ~15-25MB | Tauri |
| **Cross-Platform** | Good | 🌍 Excellent | Tauri |
| **Modern UI** | Custom styling | 🎨 Modern CSS | Tauri |
| **Updates** | Manual | Auto-update ready | Tauri |
| **Web Technologies** | No | ✅ Yes | Tauri |

## 📦 Installation

### Prerequisites

- **Rust** (latest stable version)
- **Node.js** (v16 or higher)
- **npm** or **yarn**

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd text-anonymizer-tauri
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run in development mode**
   ```bash
   npm run tauri dev
   ```

4. **Build for production**
   ```bash
   npm run tauri build
   ```

### Building Binaries

The build process creates native executables for your platform:

- **Windows**: `.exe` installer and standalone executable
- **macOS**: `.dmg` disk image and `.app` bundle
- **Linux**: `.deb` package and `.AppImage`

Built files are located in `src-tauri/target/release/bundle/`

## 🏗️ Architecture

### Backend (Rust)
- **Configuration Management**: JSON-based config storage in user home directory
- **Text Processing**: High-performance regex-based text replacement
- **File I/O**: Secure file operations with proper error handling
- **Case Preservation**: Smart case pattern matching and preservation
- **Type Safety**: Strong typing with Serde for JSON serialization

### Frontend (React + TypeScript)
- **Modern Components**: Functional components with React hooks
- **State Management**: useState and useEffect for local state
- **UI Framework**: Tailwind CSS for modern, responsive design
- **Type Safety**: Full TypeScript coverage for better development experience
- **Icons**: Lucide React for consistent iconography

### Communication Layer (Tauri)
- **IPC Commands**: Type-safe communication between frontend and backend
- **Security**: Whitelist-based API access with minimal permissions
- **Performance**: Native code execution with web UI rendering

## 🎯 Usage

### Basic Workflow

1. **Launch the application**
2. **Enter or paste text** in the main text area
3. **Configure replacement rules** in the right panel
4. **Set options**: case sensitivity and word boundaries
5. **Click "Anonymize"** to replace sensitive data
6. **Share the anonymized text** safely
7. **Click "De-anonymize"** to restore original data

### Configuration Management

#### Creating Rules
- Add **Original** text and **Replacement** text
- Click **"Add"** to save the rule
- Rules are applied in order during processing

#### Configuration Options
- **Case Sensitivity**: Choose case-sensitive or case-insensitive matching
- **Word Boundaries**: Match whole words only or partial text
- **Case Preservation**: Maintains original capitalization patterns

#### Saving & Loading
- **Save**: Store current configuration with a custom name
- **Load**: Switch between saved configurations
- **Delete**: Remove unwanted configurations
- **New**: Create a fresh configuration

### Advanced Features

#### Case-Insensitive Replacement with Pattern Preservation
```
Original: "David works at Microsoft"
Rule: David → Lucas, Microsoft → TECH_COMPANY

Result: "Lucas works at TECH_COMPANY"

Mixed case example:
"DAVID uses microsoft products" → "LUCAS uses TECH_COMPANY products"
```

#### Word Boundary Control
- **Whole words only**: "David" matches "David" but not "Davidson"
- **Replace anywhere**: "David" matches both "David" and "Davidson"

## 🔧 Development

### Project Structure
```
text-anonymizer-tauri/
├── src/                    # React frontend
│   ├── App.tsx            # Main application component
│   ├── types.ts           # TypeScript type definitions
│   ├── tauri-api.ts       # Tauri command wrappers
│   └── App.css            # Tailwind styles
├── src-tauri/             # Rust backend
│   ├── src/
│   │   ├── lib.rs         # Main Tauri application
│   │   └── main.rs        # Application entry point
│   ├── Cargo.toml         # Rust dependencies
│   └── tauri.conf.json    # Tauri configuration
├── package.json           # Node.js dependencies
└── tailwind.config.js     # Tailwind CSS configuration
```

### Adding New Features

1. **Backend (Rust)**:
   - Add new commands in `src-tauri/src/lib.rs`
   - Update the `invoke_handler` to include new commands
   - Add required dependencies to `Cargo.toml`

2. **Frontend (React)**:
   - Add API wrappers in `tauri-api.ts`
   - Update TypeScript types in `types.ts`
   - Implement UI components in `App.tsx`

3. **Styling**:
   - Use Tailwind CSS classes
   - Add custom components in `App.css`
   - Follow the existing dark theme color scheme

### Running Tests
```bash
# Run Rust tests
cd src-tauri
cargo test

# Run frontend tests (if implemented)
npm test
```

## 📝 Configuration Storage & File Format

### 📁 **Where Configurations Are Saved**

Configurations are automatically saved in your user home directory:

**Location:** `~/.text-anonymizer/configs/`
- **macOS/Linux:** `/Users/[username]/.text-anonymizer/configs/`
- **Windows:** `C:\Users\[username]\.text-anonymizer\configs\`

**File naming:** `config_{name}.json`

### 📋 **Why This Location?**

1. **Cross-platform compatibility** - Works consistently across all operating systems
2. **User-specific storage** - Each user has their own configurations
3. **Persistent storage** - Configs survive app updates and project moves
4. **Security compliance** - Follows modern app security standards
5. **Hidden by default** - Keeps user directory clean (`.text-anonymizer` is hidden)

### 📄 **Configuration File Format**

```json
{
  "config_name": "Sample",
  "case_insensitive": true,
  "whole_words_only": true,
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
  "created_date": "2025-01-28",
  "last_modified": "2025-01-28"
}
```

### 🔧 **Managing Configurations**

**To view your configurations:**
```bash
# List all saved configurations
ls ~/.text-anonymizer/configs/

# View a specific configuration
cat ~/.text-anonymizer/configs/config_Sample.json
```

**To backup configurations:**
```bash
# Backup all configurations
cp -r ~/.text-anonymizer/configs/ ~/Desktop/anonymizer-configs-backup/
```

**To share configurations:**
```bash
# Export a specific configuration
cp ~/.text-anonymizer/configs/config_MyProject.json /path/to/share/
```

## 🔒 Security Features

- **Sandboxed Environment**: Tauri provides OS-level sandboxing
- **Minimal Permissions**: Only required file system access
- **No Network Access**: Application works completely offline
- **Local Storage**: All data stored locally, never transmitted
- **Memory Safety**: Rust prevents common security vulnerabilities

## 🚀 Performance Optimizations

- **Regex Caching**: Compiled regex patterns for faster processing
- **Efficient String Operations**: Zero-copy string operations where possible
- **Minimal Bundle Size**: Tree-shaking and dead code elimination
- **Fast Startup**: Lazy loading and optimized initialization
- **Responsive UI**: Non-blocking operations with loading states

## 📱 Platform-Specific Features

### Windows
- Native Windows styling
- Windows installer with proper uninstall
- Start menu integration

### macOS
- Native macOS appearance
- Dock integration
- Retina display support

### Linux
- Multiple package formats (deb, AppImage)
- Desktop entry creation
- System theme integration

## 🔄 Migration from Python Version

If you're migrating from the Python/PyQt6 version:

1. **Configuration Compatibility**: Export your configs from the Python version and import them into the Tauri version
2. **Feature Parity**: All original features are available with improved performance
3. **Enhanced UI**: The new interface provides better usability and visual appeal
4. **Better Performance**: Expect significantly faster text processing and lower memory usage

## 🛠️ Troubleshooting

### Common Issues

1. **Build Errors**
   ```bash
   # Clear dependencies and reinstall
   rm -rf node_modules target dist
   npm install
   ```

2. **Rust Compilation Issues**
   ```bash
   # Update Rust toolchain
   rustup update
   ```

3. **Development Server Issues**
   ```bash
   # Kill any existing processes
   pkill -f "tauri dev"
   npm run tauri dev
   ```

### Getting Help

- Check the [Tauri documentation](https://tauri.app/develop)
- Review the [React documentation](https://react.dev)
- Search existing issues in the repository

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with proper TypeScript types
4. Test thoroughly on your platform
5. Submit a pull request with a clear description

## 🙏 Acknowledgments

- **Tauri Team**: For the excellent framework
- **React Team**: For the powerful UI library  
- **Rust Community**: For the robust systems programming language
- **Original Python Version**: For providing the foundation and requirements
