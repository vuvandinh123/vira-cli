import subprocess
import os
import sys
import threading
from vira.services.command_logger import CommandLogger
import platform

IS_WINDOWS = platform.system() == "Windows"

INTERACTIVE_KEYWORDS = [
    "npm", "npx", "yarn", "pnpm",
    "create-react-app", "create-next-app", "create-vite",
    "docker", "git", "vim", "nano",
    "python", "node", "irb", "php",  # REPLs
    "pip", "cargo", "go", "ruby"
]
class CommandExecutor:
    """Enhanced command executor with logging and cross-platform support"""
    
    def __init__(self, logger=None):
        self.logger = logger or CommandLogger()
    
    def execute(self, command, capture_output=True, interactive_hint=None):
        """
        Execute command with smart handling for interactive vs non-interactive.
        
        Args:
            command: Command string to execute
            capture_output: Whether to capture output (for non-interactive)
            interactive_hint: Force interactive mode (True/False/None=auto-detect)
        
        Returns:
            dict: {
                'success': bool,
                'stdout': str,
                'stderr': str,
                'exit_code': int,
                'log_entry': dict
            }
        """
        import time
        start_time = time.time()
        
        # Auto-detect or use hint
        if interactive_hint is None:
            is_interactive = self._is_interactive_command(command)
        else:
            is_interactive = interactive_hint
        
        try:
            if is_interactive or not capture_output:
                # Interactive mode: stream to console
                result = self._execute_interactive(command)
            else:
                # Non-interactive: full capture
                result = self._execute_captured(command)
            
            duration = time.time() - start_time
            
            # Log execution
            log_entry = self.logger.log_execution(
                command=command,
                success=result['success'],
                stdout=result['stdout'],
                stderr=result['stderr'],
                exit_code=result['exit_code'],
                duration=duration
            )
            
            result['log_entry'] = log_entry
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            log_entry = self.logger.log_execution(
                command=command,
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration=duration
            )
            
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1,
                'log_entry': log_entry
            }
    
    def _execute_interactive(self, command):
        """
        Execute interactive command while still capturing output.
        Cross-platform compatible (Windows, Mac, Linux).
        """
        # For commands that need real TTY (vim, nano, etc.)
        if self._needs_tty(command):
            process = subprocess.Popen(
                command,
                shell=True,
                text=True
            )
            process.wait()
            
            return {
                'success': process.returncode == 0,
                'stdout': "(interactive TTY command - output not captured)",
                'stderr': "",
                'exit_code': process.returncode
            }
        
        # For other commands - capture AND display (cross-platform)
        stdout_lines = []
        stderr_lines = []
        
        def read_stream(stream, output_list, output_stream):
            """Read from stream and both print and capture"""
            try:
                for line in iter(stream.readline, ''):
                    if not line:
                        break
                    print(line, end='', file=output_stream)
                    output_stream.flush()
                    output_list.append(line)
            except Exception:
                pass
        
        try:
            # Get shell configuration for platform
            shell_config = self._get_shell_config()
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                **shell_config
            )
            
            # Use threads to read stdout and stderr simultaneously
            # This prevents deadlocks and works on all platforms
            stdout_thread = threading.Thread(
                target=read_stream,
                args=(process.stdout, stdout_lines, sys.stdout)
            )
            stderr_thread = threading.Thread(
                target=read_stream,
                args=(process.stderr, stderr_lines, sys.stderr)
            )
            
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            
            stdout_thread.start()
            stderr_thread.start()
            
            # Wait for process to complete
            process.wait()
            
            # Wait for threads to finish reading
            stdout_thread.join(timeout=1)
            stderr_thread.join(timeout=1)
            
            return {
                'success': process.returncode == 0,
                'stdout': ''.join(stdout_lines),
                'stderr': ''.join(stderr_lines),
                'exit_code': process.returncode
            }
            
        except Exception as e:
            return {
                'success': False,
                'stdout': ''.join(stdout_lines),
                'stderr': ''.join(stderr_lines) + f"\nException: {str(e)}",
                'exit_code': -1
            }
    
    def _execute_captured(self, command):
        """Execute command with full output capture (non-interactive)"""
        try:
            shell_config = self._get_shell_config()
            
            result = subprocess.run(
                command,
                text=True,
                capture_output=True,
                timeout=300,  # 5 minute timeout to prevent hanging
                **shell_config
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout.strip() if result.stdout else "",
                'stderr': result.stderr.strip() if result.stderr else "",
                'exit_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': "",
                'stderr': "Command timeout (exceeded 5 minutes)",
                'exit_code': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': "",
                'stderr': str(e),
                'exit_code': -1
            }
    
    def _is_interactive_command(self, command):
        """Detect if command is likely interactive"""
        return any(keyword in command for keyword in INTERACTIVE_KEYWORDS)
    
    def _needs_tty(self, command):
        """Check if command needs a real TTY (like vim, nano)"""
        # TTY commands don't work well on Windows CMD/PowerShell
        if IS_WINDOWS:
            return False
        
        tty_commands = [
            "vim", "vi", "nano", "emacs",
            "less", "more", "top", "htop",
            "ssh", "telnet", "ftp"
        ]
        return any(cmd in command for cmd in tty_commands)
    
    def _get_shell_config(self):
        """Get appropriate shell configuration for the platform"""
        if IS_WINDOWS:
            # Use cmd.exe on Windows for better compatibility
            return {
                'shell': True
            }
        else:
            # Use bash on Unix-like systems if available
            return {
                'shell': True,
                'executable': '/bin/bash' if os.path.exists('/bin/bash') else None
            }
    
    def get_last_error(self):
        """Get the last error for retry/fix purposes"""
        return self.logger.get_last_error()
