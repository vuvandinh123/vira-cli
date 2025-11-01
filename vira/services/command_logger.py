from pathlib import Path
import json
import os
import platform
from datetime import datetime
from vira.config.constants import HISTORY_DIR
class CommandLogger:
    """Logger for command execution history"""
    
    def __init__(self, log_dir=None):
        if log_dir is None:
            # Default to ~/.vira-cli/logs
            log_dir = HISTORY_DIR
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "command_history.jsonl"
    
    def log_execution(self, command, success, stdout, stderr, exit_code, duration=None):
        """Log command execution to file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "success": success,
            "exit_code": exit_code,
            "stdout": stdout[:1000] if stdout else "",  # Limit to 1000 chars
            "stderr": stderr[:1000] if stderr else "",
            "duration": duration,
            "cwd": os.getcwd(),
            "platform": platform.system()
        }
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Failed to write log: {e}")
        
        return log_entry
    
    def get_last_error(self):
        """Get the last failed command from logs"""
        if not self.log_file.exists():
            return None
        
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Read from bottom up to find last error
                for line in reversed(lines):
                    entry = json.loads(line)
                    if not entry["success"]:
                        return entry
        except Exception as e:
            print(f"Failed to read log: {e}")
        
        return None
    
    def get_recent_history(self, limit=10):
        """Get recent command history"""
        if not self.log_file.exists():
            return []
        
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                recent = [json.loads(line) for line in lines[-limit:]]
                return list(reversed(recent))
        except Exception as e:
            print(f"Failed to read history: {e}")
            return []

