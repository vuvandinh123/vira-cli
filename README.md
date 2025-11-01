# 🚀 Vira CLI - AI-Powered Terminal Assistant

> Transform natural language into shell commands instantly with the power of Google Gemini AI

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](https://github.com/vuvandinh123/vira-cli)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Interactive Mode](#-interactive-mode)
- [Alias System](#-alias-system)
- [Advanced Features](#-advanced-features)
- [Architecture](#-architecture)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [FAQ](#-faq)

---

## 🌟 Overview

**Vira CLI** is an intelligent terminal assistant that bridges the gap between natural language and shell commands. Simply describe what you want to do, and Vira will generate the appropriate command for your operating system.

### Why Vira CLI?

- 🤖 **AI-Powered**: Leverages Google Gemini 2.5 for accurate command generation
- 🌍 **Multi-language**: Supports English and Vietnamese
- 💬 **Interactive Mode**: Chat with AI to get commands on-the-fly
- 📚 **Command History**: Navigate through previous queries with arrow keys
- 🔖 **Alias System**: Save frequently used commands
- 🛡️ **Safety First**: Detects dangerous commands before execution
- 📋 **Auto-copy**: Commands automatically copied to clipboard
- 🎨 **Beautiful UI**: Rich terminal interface with colors and formatting

---

## ✨ Features

### Core Features

| Feature | Description |
|---------|-------------|
| **Natural Language Processing** | Convert plain English/Vietnamese to shell commands |
| **Multi-OS Support** | Optimized for Linux, macOS, and Windows |
| **Interactive Chat** | Continuous conversation mode with command history |
| **Smart Suggestions** | Get common flags and options for each command |
| **Command Execution** | Run commands directly with confirmation |
| **Error Recovery** | AI-powered fix for failed commands |
| **Clipboard Integration** | Auto-copy commands for easy pasting |

### Advanced Features

- 🔄 **History Navigation**: Use ↑↓ arrows to browse previous queries
- 🔍 **History Search**: Press Ctrl+R to search command history
- 💾 **Persistent Config**: All settings saved in `~/.vira-cli/`
- 🎯 **Context Aware**: AI understands follow-up questions
- 🌐 **Bilingual**: Switch between English and Vietnamese
- 📦 **Model Selection**: Choose from multiple Gemini models
- 🔐 **Safe Execution**: Blocks dangerous operations by default

---

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- pip or pipx package manager
- Internet connection (for API calls)

### Method 1: Install with pipx (Recommended)

```bash
# Install pipx if you haven't
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install Vira CLI
pipx install vira-cli
```

### Method 2: Install with pip

```bash
pip install vira-cli
```

### Method 3: Install from source

```bash
# Clone repository
git clone https://github.com/vuvandinh123/vira-cli.git
cd vira-cli

# Install in development mode
pip install -e .
```

### Linux Clipboard Support (Optional but Recommended)

```bash
# For X11 (most common)
sudo apt-get install xclip

# Or
sudo apt-get install xsel

# For Wayland
sudo apt-get install wl-clipboard
```

---

## 🚀 Quick Start

### 1. First Time Setup

Run the configuration wizard:

```bash
vira --config
```

This will guide you through:
1. API Key setup
2. Model selection
3. Language preference
4. Display settings

### 2. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### 3. Your First Command

```bash
vira list all files
```

Output:
```
💭 Thinking...

✨ ls -la

✓ Copied to clipboard
▶ Run this command? [Y/n]:
```

---

## 📖 Usage Guide

### Basic Syntax

```bash
vira <your query in natural language>
```

### Examples

#### File Operations

```bash
# List files
vira list all files
vira show hidden files

# Find files
vira find files larger than 100MB
vira search for pdf files in downloads

# File management
vira create a folder named backup
vira copy all images to backup folder
vira rename all txt files to md
vira delete files older than 30 days
```

#### System Information

```bash
# CPU and Memory
vira show cpu usage
vira check memory usage
vira find process using most memory

# Disk
vira show disk space
vira find largest directories
vira check disk io

# Network
vira show ip address
vira check internet connection
vira find which process using port 8080
```

#### Git Operations

```bash
vira show git status
vira create new branch from main
vira undo last commit but keep changes
vira view commit history with graph
vira merge feature branch to main
```

#### Package Management

```bash
# Linux (Ubuntu/Debian)
vira update all packages
vira search for package containing python
vira remove package and dependencies

# macOS
vira install node using homebrew
vira update all homebrew packages

# Python
vira install requirements from file
vira create virtual environment
vira list outdated packages
```

#### Docker Operations

```bash
vira list all docker containers
vira stop all running containers
vira remove unused images
vira build docker image from dockerfile
vira run container with port mapping
```

#### Text Processing

```bash
vira find lines containing error in log file
vira count occurrences of word in file
vira remove duplicate lines from file
vira sort file by column 3
vira replace text in all files
```

---

## ⚙️ Configuration

### Configuration File

All settings are stored in: `~/.vira-cli/config.ini`

### Configuration Commands

#### Set API Key

```bash
vira --set-api-key
```

#### Change Model

```bash
vira --set-model
```

Available models:
1. `gemini-2.0-flash` - Fast, good for simple queries
2. `gemini-2.0-pro` - More accurate, better reasoning
3. `gemini-2.5-flash` - Latest fast model (default)
4. `gemini-2.5-pro` - Latest pro model, best quality

#### Change Language

```bash
vira --set-language
```

Options:
1. English (en)
2. Tiếng Việt (vi)

#### Toggle Command Suggestions

```bash
vira --set-show-suggestions
```

Options:
- Yes: Show common flags and options
- No: Only show the command

#### Full Configuration

```bash
vira --config
```

Interactive setup for all options.

### Environment Variables

Alternatively, set API key via environment:

```bash
# Temporary (current session)
export GEMINI_API_KEY="your_api_key_here"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

---

## 💬 Interactive Mode

Start a continuous chat session with AI:

```bash
vira -i
# or
vira --interactive
```

### Interactive Commands

| Command | Description |
|---------|-------------|
| `<query>` | Generate command from your query |
| `fix` | Fix the last failed command |
| `explain` | Explain the last command |
| `clear` | Clear screen |
| `help` | Show help message |
| `exit` / `quit` / `q` | Exit interactive mode |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `↑` | Previous query |
| `↓` | Next query |
| `Ctrl+R` | Search history |
| `Ctrl+C` | Cancel current input |
| `Ctrl+D` | Exit |
| `→` or `End` | Accept auto-suggestion |

### Example Session

```bash
$ vira -i
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 Interactive Terminal Helper
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type 'exit' or 'quit' to exit.
Type 'fix' to fix last error.
Type 'run <command>' to run a command.
Type 'history' to show recent commands.
💡 Use ↑↓ arrows to browse history, Ctrl+R to search

You: list all files

✨ ls -la

▶ Run this command? [Y/n]: y
total 48
drwxr-xr-x  5 user user 4096 Jan 27 10:30 .
✅ Done!

You: find large files

✨ find . -type f -size +100M

▶ Run this command? [Y/n]: n

You: explain

Explanation:
This command searches for files larger than 100MB 
starting from the current directory recursively.

You: compress folder

✨ tar -czf folder.tar.gz folder/

▶ Run this command? [Y/n]: y
tar: folder/: Cannot stat: No such file or directory
❌ Command failed

You: fix

✨ tar -czf archive.tar.gz .

▶ Run this command? [Y/n]: y
✅ Done!

You: exit
👋 Bye!
```

### History Features

All your queries are saved to: `~/.vira-cli/chat_history.txt`

**Search History:**
1. Press `Ctrl+R`
2. Type keywords
3. Press `Enter` to use the command
4. Press `Ctrl+R` again to see next match

**View History File:**
```bash
cat ~/.vira-cli/chat_history.txt
```

**Clear History:**
```bash
rm ~/.vira-cli/chat_history.txt
```

---

## 🔖 Alias System

Save frequently used commands as aliases.

### Create Alias

```bash
vira --set-alias backup="tar -czf backup-$(date +%Y%m%d).tar.gz ."
vira --set-alias update="sudo apt update && sudo apt upgrade -y"
vira --set-alias ports="netstat -tulpn | grep LISTEN"
```

### List Aliases

```bash
vira --list-alias
```

Output:
```
┌─ 📘 Alias List ─────────────────────────────────┐
│ Name    │ Command                                │
├─────────┼────────────────────────────────────────┤
│ backup  │ tar -czf backup-$(date +%Y%m%d)...     │
│ update  │ sudo apt update && sudo apt upgrade... │
│ ports   │ netstat -tulpn | grep LISTEN           │
└─────────┴────────────────────────────────────────┘
```

### Run Alias

```bash
vira backup
```

Output:
```
✨ tar -czf backup-20250127.tar.gz .

▶ Run this alias? [Y/n]:
```

### Remove Alias

```bash
vira --remove-alias backup
```

---

## 🎯 Advanced Features

### Immediate Execution

Run commands without confirmation:

```bash
vira list files --run
```

⚠️ **Warning**: Use with caution!

### Detect Interactive Commands

Vira automatically detects commands that need user input:

```bash
vira create react app 
```

Output:
```
✨ npx create-react-app my-app

⚠️  This command may require user input
▶ Run this command? [Y/n]: y

Need to install the following packages:
create-react-app@5.1.0
Ok to proceed? (y) y    # <-- You can type here!
```

### Command Options Display

When enabled, Vira shows common flags:

```bash
vira find files
```

Output:
```
✨ find . -type f

📘 Common options:
-name "*.txt" : Find files by name pattern
-size +10M : Find files larger than 10MB
-mtime -7 : Modified in last 7 days
-exec rm {} \; : Execute command on found files
-maxdepth 2 : Limit search depth
```

### Multi-language Support

**English:**
```bash
vira --set-language
> 1. English
```

**Vietnamese:**
```bash
vira --set-language
> 2. Tiếng Việt

vira liệt kê tất cả file
✨ ls -la

📘 Các tùy chọn phổ biến:
-h : Hiển thị kích thước dễ đọc
-t : Sắp xếp theo thời gian
```

---

## 🏗️ Architecture

### Project Structure

```
vira-cli/
├── cli_helper/                 # Main package
│   ├── __init__.py            # Package initialization
│   ├── main.py                # CLI entry point
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── ai.py              # Gemini AI integration
│   │   └── command.py         # Command execution
│   ├── config/                # Configuration
│   │   ├── __init__.py
│   │   ├── manager.py         # Config management
│   │   └── constants.py       # Constants
│   ├── features/              # Features
│   │   ├── __init__.py
│   │   ├── alias.py           # Alias management
│   │   ├── chat.py            # Interactive mode
│   │   └── history.py         # Command history
│   └── utils/                 # Utilities
│       ├── __init__.py
│       ├── console.py         # Rich console helpers
│       └── system.py          # OS detection, clipboard
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── setup.py                   # Package setup
├── requirements.txt           # Dependencies
├── README.md                  # Main documentation
└── LICENSE                    # MIT License
```

### Key Components

#### 1. AI Engine (`core/ai.py`)
- Handles Gemini API communication
- Generates commands from natural language
- Manages chat sessions

#### 2. Config Manager (`config/manager.py`)
- Loads/saves configuration
- Manages API keys, models, settings
- Handles aliases

#### 3. Command Executor (`core/command.py`)
- Executes shell commands
- Supports interactive commands
- Safety checks for dangerous operations

#### 4. Interactive Chat (`features/chat.py`)
- Prompt toolkit integration
- Command history with search
- Auto-suggestion from history

#### 5. Console Utilities (`utils/console.py`)
- Rich terminal formatting
- Color-coded messages
- Tables and panels

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Command not found: vira

**Solution:**
```bash
# Check if installed
pipx list | grep vira-cli

# Reinstall
pipx reinstall vira-cli

# Or add to PATH
export PATH="$PATH:$HOME/.local/bin"
```

#### 2. API Key Error

**Error:**
```
❌ No API key found. Run: vira --config
```

**Solution:**
```bash
# Method 1: Interactive setup
vira --config

# Method 2: Direct set
vira --set-api-key

# Method 3: Environment variable
export GEMINI_API_KEY="your_key_here"
```

#### 3. Clipboard Error

**Error:**
```
⚠️ Could not copy to clipboard
```

**Solution:**
```bash
# Linux X11
sudo apt-get install xclip

# Linux Wayland
sudo apt-get install wl-clipboard

# macOS (should work by default)
# Windows (should work by default)
```

#### 4. Interactive Commands Stuck

**Problem:** Commands like `npm install` hang without accepting input.

**Solution:** Already fixed in version 2.1.0. Update:
```bash
pipx upgrade vira-cli
```

#### 5. Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'prompt_toolkit'
```

**Solution:**
```bash
pip install prompt-toolkit rich pyperclip python-dotenv google-generativeai
```

#### 6. Permission Denied

**Error:**
```
Permission denied: /home/user/.vira-cli/config.ini
```

**Solution:**
```bash
chmod 600 ~/.vira-cli/config.ini
# or delete and reconfigure
rm -rf ~/.vira-cli
vira --config
```

### Debug Mode

Enable verbose logging:

```bash
export VIRA_DEBUG=1
vira your query
```

View logs:
```bash
cat ~/.vira-cli/vira.log
```

### Getting Help

1. **Check Documentation**: [GitHub Wiki](https://github.com/vuvandinh123/vira-cli/wiki)
2. **Report Issues**: [GitHub Issues](https://github.com/vuvandinh123/vira-cli/issues)
3. **Community**: [Discussions](https://github.com/vuvandinh123/vira-cli/discussions)

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Development Setup

```bash
# Clone repository
git clone https://github.com/vuvandinh123/vira-cli.git
cd vira-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Write tests

---

## ❓ FAQ

### General Questions

**Q: Is Vira CLI free?**  
A: Yes, Vira CLI is open-source (MIT License). However, you need a Google Gemini API key, which has a free tier.

**Q: Does it work offline?**  
A: No, Vira requires internet connection to communicate with Gemini API.

**Q: Which operating systems are supported?**  
A: Linux, macOS, and Windows. Commands are optimized for each OS.

**Q: Can I use it in scripts?**  
A: Yes, use `--run` flag for non-interactive execution:
```bash
vira list files --run > output.txt
```

### Usage Questions

**Q: How do I save my favorite commands?**  
A: Use the alias system:
```bash
vira --set-alias mybackup="tar -czf backup.tar.gz ."
```

**Q: Can it execute commands automatically?**  
A: Yes, use `--run` flag, but be careful:
```bash
vira delete old logs --run  # No confirmation!
```

**Q: How to switch languages?**  
A: Run `vira --set-language` and choose your language.

**Q: Does it support multiple commands?**  
A: Currently one command per query. Use aliases for command chains.

### Technical Questions

**Q: Which AI model should I use?**  
A: 
- `gemini-2.5-flash`: Fast, good for simple commands (default)
- `gemini-2.5-pro`: Best quality, slower, for complex queries

**Q: How is my data stored?**  
A: All data stored locally in `~/.vira-cli/`:
- `config.ini`: Settings and API key
- `chat_history.txt`: Query history
- `vira.log`: Debug logs (if enabled)

**Q: Is my API key secure?**  
A: API key is stored with 600 permissions (owner read/write only). Never share your config file.

**Q: Can I use my own AI model?**  
A: Currently only Gemini models are supported. Custom model support is planned.

### Troubleshooting

**Q: Commands are slow?**  
A: 
1. Check internet connection
2. Switch to faster model (gemini-2.5-flash)
3. Use alias for frequent commands

**Q: Getting wrong commands?**  
A:
1. Be more specific in your query
2. Switch to pro model for better accuracy
3. Report issue with examples

**Q: History not working?**  
A: Check if `~/.vira-cli/chat_history.txt` is writable:
```bash
ls -la ~/.vira-cli/
chmod 600 ~/.vira-cli/chat_history.txt
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini**: For providing the AI capabilities
- **Rich**: For beautiful terminal formatting
- **Prompt Toolkit**: For interactive terminal features
- **Contributors**: Everyone who has contributed to this project

---

## 📞 Contact & Support

- **Author**: Vũ Văn Định
- **Email**: vuvandinh203@gmail.com
- **GitHub**: [@vuvandinh123](https://github.com/vuvandinh123)
- **Issues**: [Report bugs](https://github.com/vuvandinh123/vira-cli/issues)
- **Discussions**: [Community forum](https://github.com/vuvandinh123/vira-cli/discussions)


---

## 📊 Statistics

- **Version**: 2.1.0
- **Python Version**: 3.8+
- **Dependencies**: 5 core packages
- **Code Lines**: ~2,500
- **Test Coverage**: 85%
- **Downloads**: 🚀 Growing!

---

## 🌟 Star History

If you find Vira CLI useful, please give it a star on GitHub! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=vuvandinh123/vira-cli&type=Date)](https://star-history.com/#vuvandinh123/vira-cli&Date)

---

**Made with ❤️ by Vũ Văn Định**

*Happy Commanding! 🚀*