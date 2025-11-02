from vira.config.manager import ConfigManager
from vira.config.constants import AVAILABLE_MODELS, SUPPORTED_LANGUAGES, GEMINI_API_URL

from vira.utils.console import (
    console, print_error, print_success, print_info,
)

def setup_configuration(config: ConfigManager, os_type: str):
    """Interactive configuration setup"""
    console.rule("[bold cyan]⚙️ Configuration Mode")

    # Show current configuration option
    show_now = input("Show current configuration? [Y/n]: ").strip().lower() or "y"
    if show_now in ("y", "yes"):
        current_model = config.get_model()
        current_lang = config.get_language()
        current_show_sugg = config.get_show_suggestions()
        current_api = config.get_api_key() or ""
        if current_api:
            if len(current_api) > 8:
                masked_api = f"{current_api[:4]}...{current_api[-4:]}"
            else:
                masked_api = "***"
        else:
            masked_api = "(not configured)"
        console.print("\n[bold]Settings:[/bold]")
        console.print(f"  Model: {current_model}")
        console.print(f"  Language: {current_lang}")
        console.print(f"  Show suggestions: {current_show_sugg}")
        console.print(f"  API key: {masked_api}")

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
