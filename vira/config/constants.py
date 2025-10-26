"""
Constants and default values
"""
from pathlib import Path

# Directories
CONFIG_DIR = Path.home() / ".cli-helper"
CONFIG_FILE = CONFIG_DIR / "config.ini"
HISTORY_FILE = CONFIG_DIR / "history.json"
FAVORITES_FILE = CONFIG_DIR / "favorites.json"

# Default settings
DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_LANGUAGE = "en"
DEFAULT_SHOW_SUGGESTIONS = True

# Available models
AVAILABLE_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-pro",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "vi": "Tiếng Việt",
}

# API
GEMINI_API_URL = "https://aistudio.google.com/app/apikey"