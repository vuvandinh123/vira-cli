"""
Auto-fix feature for failed commands
"""
from vira.core.command import get_last_error, execute_with_log
from vira.utils.console import (
    console, print_error, print_success, 
    print_command, print_thinking, confirm
)


class CommandFixer:
    """Automatically fix failed commands using AI"""
    
    def __init__(self, ai_assistant, os_type):
        self.ai = ai_assistant
        self.os_type = os_type
    
    def fix_last_error(self, max_attempts=3):
        """
        Try to fix the last failed command.
        
        Args:
            max_attempts: Maximum number of fix attempts
        
        Returns:
            bool: True if fixed successfully
        """
        # Get last error
        last_error = get_last_error()
        
        if not last_error:
            print_error("No previous error found to fix")
            return False
        
        console.print("\n[bold red]Last failed command:[/bold red]")
        console.print(f"[dim]Command:[/dim] {last_error['command']}")
        console.print(f"[dim]Exit code:[/dim] {last_error['exit_code']}")
        
        if last_error['stderr']:
            console.print(f"[dim]Error output:[/dim]\n{last_error['stderr'][:500]}")
        
        if last_error['stdout']:
            console.print(f"[dim]Output:[/dim]\n{last_error['stdout'][:500]}")
        
        console.print()
        
        if not confirm("🔧 Try to fix this error?"):
            return False
        
        # Attempt to fix
        for attempt in range(1, max_attempts + 1):
            console.print(f"\n[bold]Attempt {attempt}/{max_attempts}[/bold]")
            print_thinking("Analyzing error and generating fix...")
            
            try:
                fixed_command, explanation = self._generate_fix(last_error)
                
                if not fixed_command:
                    print_error("AI couldn't generate a fix")
                    return False
                
                # Show explanation first
                if explanation:
                    console.print(f"\n[yellow]💡 Analysis:[/yellow] {explanation}\n")
                
                # Then show the fixed command
                print_command(fixed_command)
                
                if not confirm("▶ Try this fix?"):
                    continue
                
                # Execute the fix
                result = execute_with_log(fixed_command, capture_output=False)
                
                if result['success']:
                    print_success("✓ Command executed successfully!")
                    return True
                else:
                    console.print("[yellow]Fix attempt failed, trying again...[/yellow]")
                    # Update last_error for next iteration
                    last_error = result['log_entry']
                    
            except Exception as e:
                print_error(f"Error during fix attempt: {e}")
        
        print_error(f"Could not fix after {max_attempts} attempts")
        return False
    
    def _generate_fix(self, error_log):
        """
        Ask AI to generate a fixed version of the command.
        
        Args:
            error_log: Dictionary with command, stderr, stdout, etc.
        
        Returns:
            tuple: (fixed_command: str, explanation: str)
        """
        # Build context for AI
        error_context = f"""
    The following command failed:
    Command: {error_log['command']}
    Exit code: {error_log['exit_code']}
    Working directory: {error_log.get('cwd', 'unknown')}

    Error output (stderr):
    {error_log['stderr'][:1000]}

    Standard output (stdout):
    {error_log['stdout'][:1000]}
    """
        
        try:
            # Use specialized error analysis function
            fixed_command, explanation = self.ai.analyze_and_fix_error(
                error_context=error_context,
                os_type=self.os_type,
            )
            
            if not fixed_command:
                return None, None
                
            return fixed_command, explanation
            
        except Exception as e:
            print_error(f"AI error: {e}")
            return None, None
    def suggest_fix(self, command, error_output):
        """
        Suggest a fix for a specific command and error.
        (Alternative method that doesn't rely on log history)
        
        Args:
            command: The failed command
            error_output: The error message
        
        Returns:
            tuple: (fixed_command: str, explanation: str)
        """
        print_thinking("Analyzing error...")
        
        context = f"""
This command failed:
{command}

With this error:
{error_output}

Please provide:
1. A brief explanation of what went wrong (1-2 sentences max)
2. A corrected version of the command

Format your response EXACTLY like this:
EXPLANATION: <brief explanation here>
COMMAND: <fixed command here>
"""
        
        try:
            response, _ = self.ai.generate_command(
                query=context,
                os_type=self.os_type,
                show_options=False
            )
            
            # Parse response
            explanation = ""
            fixed_command = response
            
            if "EXPLANATION:" in response and "COMMAND:" in response:
                parts = response.split("COMMAND:")
                if len(parts) == 2:
                    explanation = parts[0].replace("EXPLANATION:", "").strip()
                    fixed_command = parts[1].strip()
            elif "\n" in response:
                lines = response.split("\n", 1)
                if len(lines) == 2:
                    explanation = lines[0].strip()
                    fixed_command = lines[1].strip()
            
            return fixed_command, explanation
            
        except Exception as e:
            print_error(f"Could not generate fix: {e}")
            return None, None


def interactive_fix_loop(ai_assistant, os_type):
    """
    Interactive loop for fixing commands.
    Keeps trying until success or user quits.
    """
    fixer = CommandFixer(ai_assistant, os_type)
    
    while True:
        success = fixer.fix_last_error(max_attempts=1)
        
        if success:
            break
        
        if not confirm("🔄 Try another fix approach?"):
            break
    
    return success