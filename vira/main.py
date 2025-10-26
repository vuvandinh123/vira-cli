"""
Main entry point
"""
import argparse
import sys

from vira.config.manager import ConfigManager
from vira.config.constants import AVAILABLE_MODELS, SUPPORTED_LANGUAGES, GEMINI_API_URL
from vira.core.ai import AIAssistant
from vira.core.command import execute_command
from vira.features.alias import AliasManager
from vira.features.chat import ChatMode
from vira.utils.system import detect_os, copy_to_clipboard
from vira.utils.console import (
    console, print_error, print_success, print_info,
    print_command, print_thinking, print_options, confirm
)



def setup_configuration(config: ConfigManager, os_type: str):
    """Interactive configuration setup"""
    console.rule("[bold cyan]⚙️ Configuration Mode")
    
    # Select model
    console.print("\n[bold]Select Gemini model:[/bold]")
    for i, model in enumerate(AVAILABLE_MODELS, 1):
        console.print(f"  {i}. {model}")
    
    choice = input("\nSelect model (1-4): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(AVAILABLE_MODELS):
        model_name = AVAILABLE_MODELS[int(choice) - 1]
    else:
        model_name = AVAILABLE_MODELS[0]
    
    # API Key
    console.print(f"\n🔑 Get API key at: [cyan]{GEMINI_API_URL}[/cyan]")
    api_key = input("Enter Gemini API key: ").strip()
    
    if not api_key:
        print_error("API key cannot be empty")
        return
    
    # Language
    console.print("\n🌐 Select language:")
    for i, (code, name) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
        console.print(f"  {i}. {name} ({code})")
    
    lang_choice = input("Select language [1/2]: ").strip() or "1"
    language = list(SUPPORTED_LANGUAGES.keys())[int(lang_choice) - 1 if lang_choice.isdigit() else 0]
    
    # Show suggestions
    show_sugg = input("\n💡 Show command suggestions? [Y/n]: ").strip().lower() or "y"
    show_suggestions = show_sugg in ["y", "yes"]
    
    # Save
    config.set_api_key(api_key)
    config.set_model(model_name)
    config.set_language(language)
    config.set_show_suggestions(show_suggestions)
    
    print_success("Configuration saved!")
    print_info(f"Model: {model_name} | Language: {language} | OS: {os_type}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="🤖 CLI Helper - AI-powered terminal assistant"
    )
    
    # Main arguments
    parser.add_argument("query", nargs="*", help="Your natural language query")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive chat mode")
    parser.add_argument("--run", action="store_true", help="Run command immediately")
    parser.add_argument("--config", action="store_true", help="Configure settings")
    
    # Configuration
    parser.add_argument("--set-api-key", nargs="?", const=True, help="Set API key")
    parser.add_argument("--set-model", nargs="?", const=True, help="Set model")
    parser.add_argument("--set-language", nargs="?", const=True, help="Set language")
    parser.add_argument("--set-show-suggestions", nargs="?", const=True, help="Toggle suggestions")
    
    # Alias management
    parser.add_argument("--set-alias", help="Set alias (name=command)")
    parser.add_argument("--remove-alias", help="Remove alias")
    parser.add_argument("--list-alias", action="store_true", help="List aliases")
    
    args = parser.parse_args()
    
    # Initialize
    config = ConfigManager()
    alias_manager = AliasManager(config)
    os_type = detect_os()
    
    # Handle configuration commands
    if args.config:
        setup_configuration(config, os_type)
        return
    
    if args.set_api_key:
        new_key = input("Enter new API key: ").strip()
        if new_key:
            config.set_api_key(new_key)
            print_success("API key updated")
        return
    
    if args.set_model:
        console.print("Select model:")
        for i, m in enumerate(AVAILABLE_MODELS, 1):
            console.print(f"  {i}. {m}")
        choice = input("Choice (1-4): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(AVAILABLE_MODELS):
            config.set_model(AVAILABLE_MODELS[int(choice) - 1])
            print_success(f"Model set to {AVAILABLE_MODELS[int(choice) - 1]}")
        return
    
    # Handle alias commands
    if args.set_alias:
        alias_manager.set(args.set_alias)
        return
    
    if args.remove_alias:
        alias_manager.remove(args.remove_alias)
        return
    
    if args.list_alias:
        alias_manager.list()
        return
    
    # Check if query is an alias
    if args.query and len(args.query) == 1:
        alias_cmd = alias_manager.get(args.query[0])
        if alias_cmd:
            print_command(alias_cmd)
            if confirm("▶ Run this alias?"):
                execute_command(alias_cmd, capture_output=False)
            return
    
    # Check API key
    api_key = config.get_api_key()
    if not api_key:
        print_error("No API key found. Run: how --config")
        return
    
    # Initialize AI
    model_name = config.get_model()
    ai = AIAssistant(api_key, model_name)
    
    # Interactive mode
    if args.interactive:
        chat = ChatMode(ai, os_type)
        chat.start()
        return
    
    # Normal query mode
    if not args.query:
        print_error("Please provide a query or use -i for chat mode")
        return
    
    query = " ".join(args.query)
    language = config.get_language()
    show_suggestions = config.get_show_suggestions()
    
    print_thinking()
    
    try:
        command, options = ai.generate_command(query, os_type, language, show_suggestions)
        
        # Display
        print_command(command)
        
        if show_suggestions:
            print_options(options)
        
        # Copy to clipboard
        success, msg = copy_to_clipboard(command)
        console.print(f"[dim]{msg}[/dim]")
        
        # Execute
        if args.run or confirm("▶ Run this command?"):
            execute_command(command, capture_output=False)
    
    except Exception as e:
        print_error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()