"""
Interactive chat mode with history support
"""
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

from ..core.ai import AIAssistant
from ..core.command import execute_with_log, get_last_error, get_command_history
from ..utils.console import console, print_error, print_command, confirm, print_success
from ..config.constants import CONFIG_DIR
from ..features.fix import CommandFixer


class ChatMode:
    """Interactive chat with AI and command history"""
    
    def __init__(self, ai: AIAssistant, os_type: str):
        self.ai = ai
        self.os_type = os_type
        self.fixer = CommandFixer(ai, os_type)
        
        # Setup history file
        history_file = CONFIG_DIR / "chat_history.txt"
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create prompt session with history
        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
        )
        
        # Custom style for prompt
        self.style = Style.from_dict({
            'prompt': '#00ff00 bold',  # Green bold
        })
    
    def start(self):
        """Start interactive chat"""
        console.rule("[bold cyan]💬 Interactive Terminal Helper")
        console.print("[yellow]Type 'exit' or 'quit' to exit.[/yellow]")
        console.print("[yellow]Type 'fix' to fix last error.[/yellow]")
        console.print("[yellow]Type 'history' to show recent commands.[/yellow]")
        console.print("[yellow]Type 'run <command>' to run a command.[/yellow]")
        console.print("[dim]💡 Use ↑↓ arrows to browse history, Ctrl+R to search[/dim]\n")
        
        while True:
            try:
                # Use prompt_toolkit for input with history
                user_input = self.session.prompt(
                    [('class:prompt', 'You: ')],
                    style=self.style
                ).strip()
                
                if not user_input:
                    continue
                
                # Run command directly
                if user_input.lower().startswith("run "):
                    command = user_input[4:].strip()
                    if not command:
                        print_error("No command provided after 'run'")
                        continue
                    
                    self._execute_command(command)
                    continue
                
                # Exit commands
                if user_input.lower() in ["exit", "quit", "q"]:
                    console.print("[green]👋 Bye![/green]")
                    break
                
                # Fix last error using enhanced fixer
                if user_input.lower() == "fix":
                    self.fixer.fix_last_error(max_attempts=3)
                    continue
                
                # Show command history
                if user_input.lower() == "history":
                    self._show_history()
                    continue
                
                # # Explain last command
                # if user_input.lower() == "explain":
                #     last_error = get_last_error()
                #     if not last_error:
                #         print_error("No previous command to explain")
                #         continue
                    
                #     self._explain_command(last_error['command'])
                #     continue
                
                # Clear screen
                if user_input.lower() == "clear":
                    console.clear()
                    continue
                
                # Show help
                if user_input.lower() == "help":
                    self._show_help()
                    continue
                
                # Generate command from query
                command = self._generate_command(user_input)
                if command:
                    print_command(command)
                    self._execute_if_confirmed(command)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except EOFError:
                console.print("\n[green]👋 Bye![/green]")
                break
            except Exception as e:
                print_error(f"Error: {e}")
    
    def _generate_command(self, query):
        """Generate command from natural language query"""
        prompt = f"""You are an expert {self.os_type} terminal assistant.

**CRITICAL RULES:**
1. Return ONLY the shell command itself
2. NO explanations, NO markdown, NO extra text
3. Just the pure executable command
4. One line only

User query: "{query}"
Command:"""
        
        try:
            # Use direct model call instead of chat to avoid context pollution
            response = self.ai.model.generate_content(prompt)
            command = response.text.strip()
            
            # Clean up
            command = self._clean_command(command)
            
            return command
            
        except Exception as e:
            print_error(f"Failed to generate command: {e}")
            return None
    
    def _execute_command(self, command):
        """Execute command with enhanced logging"""
        # Handle multi-line commands
        commands = [c.strip() for c in command.split("\n") if c.strip()]
        full_command = " && ".join(commands)
        
        console.print(f"[dim]Executing: {full_command}[/dim]")
        
        # Use enhanced executor with logging
        # capture_output=False means output goes directly to terminal
        result = execute_with_log(full_command, capture_output=False)
        
        # Print status message
        if result['success']:
            console.print("[green]✅ Done![/green]")
        else:
            console.print("[red]❌ Command failed[/red]")
            console.print("[yellow]💡 Type 'fix' to attempt auto-fix[/yellow]")
    
    def _execute_if_confirmed(self, command):
        """Execute command after confirmation with enhanced logging"""
        if confirm("▶ Run this command?"):
            self._execute_command(command)
    
    def _explain_command(self, command):
        """Explain a command"""
        prompt = f"""Explain this {self.os_type} command briefly:

Command: {command}

Provide a short explanation (2-3 sentences max)."""
        
        try:
            response = self.ai.model.generate_content(prompt)
            explanation = response.text.strip()
            console.print(f"\n[bold cyan]Explanation:[/bold cyan]")
            console.print(f"{explanation}\n")
            
        except Exception as e:
            print_error(f"Failed to explain: {e}")
    
    def _show_history(self):
        """Show recent command history"""
        history = get_command_history(limit=15)
        
        if not history:
            console.print("[dim]No command history found[/dim]")
            return
        
        console.print("\n[bold cyan]Recent Commands:[/bold cyan]\n")
        
        for i, entry in enumerate(history, 1):
            status = "✓" if entry['success'] else "✗"
            color = "green" if entry['success'] else "red"
            
            console.print(f"[{color}]{status}[/{color}] [{i}] {entry['command']}")
            
            # Show timestamp
            timestamp = entry['timestamp'].split('T')[1].split('.')[0]  # HH:MM:SS
            console.print(f"    [dim]{timestamp} | Exit: {entry['exit_code']}[/dim]")
            
            # Show error if failed
            if not entry['success'] and entry['stderr']:
                error_preview = entry['stderr'][:80]
                if len(entry['stderr']) > 80:
                    error_preview += "..."
                console.print(f"    [red]Error: {error_preview}[/red]")
            
            console.print()
    
    def _show_help(self):
        """Show help message"""
        console.print("""
[bold cyan]Available Commands:[/bold cyan]
  [green]exit, quit, q[/green]    - Exit interactive mode
  [green]fix[/green]               - Fix the last failed command (auto-retry)
  [green]explain[/green]           - Explain the last command
  [green]history[/green]           - Show recent command history
  [green]clear[/green]             - Clear screen
  [green]help[/green]              - Show this help message
  [green]run <command>[/green]    - Run a command directly (with logging)
  [green]<any text>[/green]       - Generate command from your query

[bold cyan]Keyboard Shortcuts:[/bold cyan]
  [green]↑ / ↓[/green]             - Browse command history
  [green]Ctrl+R[/green]            - Search history (type to filter)
  [green]Ctrl+C[/green]            - Cancel current input
  [green]Ctrl+D[/green]            - Exit

[bold cyan]Features:[/bold cyan]
  • All commands are automatically logged
  • Failed commands can be auto-fixed with AI
  • Command history persists across sessions
  • Interactive commands (npm create, etc.) are supported
""")
    
    def _clean_command(self, command):
        """Clean up command from markdown and extra text"""
        # Remove markdown code blocks
        if command.startswith("```") and command.endswith("```"):
            command = command[3:-3].strip()
        if command.startswith("```"):
            lines = command.split("\n")
            command = "\n".join(lines[1:]).strip()
        if command.endswith("```"):
            lines = command.split("\n")
            command = "\n".join(lines[:-1]).strip()
        
        # Remove language specifiers
        for lang in ["bash", "sh", "shell", "zsh"]:
            if command.startswith(lang + "\n"):
                command = command[len(lang)+1:].strip()
        
        # Remove backticks
        command = command.replace("`", "")
        
        # Get only first line if multiple lines
        if "\n" in command:
            command = command.split("\n")[0].strip()
        
        return command