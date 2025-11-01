"""
Command execution utilities with logging
Cross-platform support for Windows, macOS, and Linux
"""
import platform
from vira.services.command_logger import CommandLogger
from vira.services.command_executor import CommandExecutor
# Detect OS
IS_WINDOWS = platform.system() == "Windows"

    
# Singleton instances
_default_logger = CommandLogger()
_default_executor = CommandExecutor(_default_logger)


def execute_command(command, capture_output=True):
    """
    Legacy wrapper for backward compatibility.
    Returns: (success: bool, stdout: str, stderr: str)
    """
    result = _default_executor.execute(command, capture_output)
    return result['success'], result['stdout'], result['stderr']


def execute_with_log(command, capture_output=True):
    """
    Enhanced execution that returns full result with log entry.
    Returns: dict with success, stdout, stderr, exit_code, log_entry
    """
    return _default_executor.execute(command, capture_output)


def get_last_error():
    """Get the last failed command for AI to analyze and fix"""
    return _default_executor.get_last_error()


def get_command_history(limit=10):
    """Get recent command history"""
    return _default_logger.get_recent_history(limit)


def is_safe_command(command):
    """
    Check if command is safe to execute
    Returns: (is_safe: bool, reason: str)
    """
    dangerous_patterns = [
        "rm -rf /",
        "dd if=",
        "mkfs",
        ":(){:|:&};:",
        "> /dev/sd",
        "chmod -R 777 /",
    ]
    
    # Windows-specific dangerous commands
    if IS_WINDOWS:
        dangerous_patterns.extend([
            "format c:",
            "del /f /s /q c:\\",
            "rd /s /q c:\\",
        ])
    
    for pattern in dangerous_patterns:
        if pattern.lower() in command.lower():
            return False, f"Dangerous pattern detected: {pattern}"
    
    return True, ""