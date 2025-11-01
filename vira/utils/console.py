"""
Console utilities using Rich
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_error(message):
    """Print error message"""
    console.print(f"[bold red]❌ {message}[/bold red]")


def print_success(message):
    """Print success message"""
    console.print(f"[green]✅ {message}[/green]")


def print_warning(message):
    """Print warning message"""
    console.print(f"[yellow]⚠️  {message}[/yellow]")


def print_info(message):
    """Print info message"""
    console.print(f"[cyan]ℹ️  {message}[/cyan]")


def print_command(command):
    """Print command with nice formatting"""
    console.print(f"\n✨ [bold green]{command}[/bold green]\n")


def print_thinking(text="Thinking..."):
    """Print thinking message"""
    console.print(f"💭 [dim]{text}[/dim]")


def print_options(options_text):
    """Print command options"""
    if options_text and options_text.lower() != "none":
        console.print("[bold cyan]📘 Common options:[/bold cyan]")
        console.print(options_text + "\n")


def print_table(title, headers, rows):
    """Print a table"""
    table = Table(title=title, show_header=True)
    
    for header in headers:
        table.add_column(header)
    
    for row in rows:
        table.add_row(*row)
    
    console.print(table)


def print_panel(content, title="", border_style="cyan"):
    """Print content in a panel"""
    console.print(Panel(content, title=title, border_style=border_style))


def confirm(message, default=True):
    """Ask for confirmation"""
    suffix = "[Y/n]" if default else "[y/N]"
    response = console.input(f"{message} {suffix}: ").strip().lower()
    
    if not response:
        return default
    
    return response in ["y", "yes"]