"""
Configuration management
"""
import os
import configparser
from pathlib import Path
from .constants import (
    CONFIG_DIR, CONFIG_FILE, DEFAULT_MODEL,
    DEFAULT_LANGUAGE, DEFAULT_SHOW_SUGGESTIONS
)


class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            self.config.read(CONFIG_FILE)
        
        # Ensure all sections exist
        for section in ["config", "alias", "settings"]:
            if section not in self.config:
                self.config[section] = {}
        
        # Set defaults
        if "model" not in self.config["config"]:
            self.config["config"]["model"] = DEFAULT_MODEL
        if "language" not in self.config["settings"]:
            self.config["settings"]["language"] = DEFAULT_LANGUAGE
        if "show_suggestions" not in self.config["settings"]:
            self.config["settings"]["show_suggestions"] = str(DEFAULT_SHOW_SUGGESTIONS).lower()
    
    def save(self):
        """Save configuration to file"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            self.config.write(f)
        CONFIG_FILE.chmod(0o600)
    
    def get_api_key(self):
        """Get API key from env or config"""
        return os.getenv("GEMINI_API_KEY") or self.config["config"].get("api_key")
    
    def set_api_key(self, key):
        """Set API key"""
        self.config["config"]["api_key"] = key
        self.save()
    
    def get_model(self):
        """Get model name"""
        return self.config["config"].get("model", DEFAULT_MODEL)
    
    def set_model(self, model):
        """Set model name"""
        self.config["config"]["model"] = model
        self.save()
    
    def get_language(self):
        """Get language"""
        return self.config["settings"].get("language", DEFAULT_LANGUAGE)
    
    def set_language(self, lang):
        """Set language"""
        self.config["settings"]["language"] = lang
        self.save()
    
    def get_show_suggestions(self):
        """Get show_suggestions setting"""
        return self.config["settings"].getboolean("show_suggestions", DEFAULT_SHOW_SUGGESTIONS)
    
    def set_show_suggestions(self, value):
        """Set show_suggestions"""
        self.config["settings"]["show_suggestions"] = str(value).lower()
        self.save()
    
    # Alias methods
    def get_alias(self, name):
        """Get alias by name"""
        return self.config["alias"].get(name)
    
    def set_alias(self, name, command):
        """Set alias"""
        self.config["alias"][name] = command
        self.save()
    
    def remove_alias(self, name):
        """Remove alias"""
        if name in self.config["alias"]:
            del self.config["alias"][name]
            self.save()
            return True
        return False
    
    def list_aliases(self):
        """Get all aliases"""
        return dict(self.config["alias"])