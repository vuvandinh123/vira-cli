"""
System utilities
"""
import sys
import pyperclip


def detect_os():
    """Detect operating system"""
    if sys.platform.startswith("linux"):
        return "Linux"
    elif sys.platform == "darwin":
        return "macOS"
    elif sys.platform == "win32":
        return "Windows"
    return "Linux"


def copy_to_clipboard(text):
    """
    Copy text to clipboard
    Returns: (success: bool, message: str)
    """
    try:
        pyperclip.copy(text)
        return True, "✓ Copied to clipboard"
    except pyperclip.PyperclipException:
        return False, "ℹ️  Install xclip for auto-copy (sudo apt install xclip)"
    except Exception as e:
        return False, f"⚠️  Could not copy: {e}"