"""
Command execution utilities
"""
import subprocess

import subprocess

INTERACTIVE_KEYWORDS = ["npm", "npx", "yarn", "create-react-app"]

def execute_command(command, capture_output=True):
    """
    Smart shell executor for CLI AI.
    Detects if command is interactive and prompts user before running.

    Returns:
        success (bool), stdout (str), stderr (str)
    """
    # Detect if command is interactive
    interactive = any(cmd in command for cmd in INTERACTIVE_KEYWORDS)

    try:
        # Nếu không cần capture output HOẶC là interactive command
        if not capture_output or interactive:
            # Chạy trực tiếp, không capture output
            process = subprocess.Popen(
                command,
                shell=True,
                text=True
            )
            process.communicate()
            success = process.returncode == 0
            return success, "", ""
        else:
            # Capture output cho non-interactive command
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True
            )
            return (
                result.returncode == 0,
                result.stdout.strip() if result.stdout else "",
                result.stderr.strip() if result.stderr else ""
            )
    except Exception as e:
        return False, "", str(e)

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
    
    for pattern in dangerous_patterns:
        if pattern in command:
            return False, f"Dangerous pattern detected: {pattern}"
    
    return True, ""