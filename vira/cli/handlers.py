"""
Vira CLI Application
"""
import sys

from vira.config.manager import ConfigManager
from vira.config.constants import AVAILABLE_MODELS
from vira.core.ai import AIAssistant
from vira.core.command import execute_command
from vira.features.alias import AliasManager
from vira.features.chat import ChatMode
from vira.utils.system import detect_os, copy_to_clipboard
from vira.utils.console import (
    console, print_error, print_success, print_info,
    print_command, print_thinking, print_options, confirm
)
from vira.utils.helper import setup_configuration


class ViraApplication:
    """Main Vira CLI Application"""
    
    def __init__(self):
        """Initialize application"""
        self.config = ConfigManager()
        self.alias_manager = AliasManager(self.config)
        self.os_type = detect_os()
        self.ai = None
    
    def run(self, args):
        """Main application entry point"""
        # Show current settings
        if args.setting:
            self._show_settings()
            return
        
        # Handle configuration commands
        if args.config:
            self._configure()
            return
        
        if args.set_api_key:
            self._set_api_key()
            return
        
        if args.set_model:
            self._set_model()
            return
        
        # Handle alias commands
        if args.set_alias:
            self.alias_manager.set(args.set_alias)
            return
        
        if args.remove_alias:
            self.alias_manager.remove(args.remove_alias)
            return
        
        if args.list_alias:
            self.alias_manager.list()
            return
        
        # Check if query is an alias
        if args.query and len(args.query) == 1:
            if self._execute_alias(args.query[0]):
                return
        
        # Validate API key
        api_key = self.config.get_api_key()
        if not api_key:
            print_error("No API key found. Run: how --config")
            return
        
        # Initialize AI
        self._initialize_ai(api_key)
        
        # Interactive mode
        if args.interactive:
            self._start_chat_mode()
            return
        
        # Normal query mode
        if not args.query:
            print_error("Please provide a query or use -i for chat mode")
            return
        
        query = " ".join(args.query)
        self._handle_query(query, run_directly=args.run)
    
    def _show_settings(self):
        """Display current settings"""
        current_model = self.config.get_model()
        current_lang = self.config.get_language()
        current_show_sugg = self.config.get_show_suggestions()
        current_api = self.config.get_api_key() or ""
        
        if current_api:
            if len(current_api) > 8:
                masked_api = f"{current_api[:4]}...{current_api[-4:]}"
            else:
                masked_api = "***"
        else:
            masked_api = "(chưa cấu hình)"
        
        aliases = self.config.list_aliases()
        
        console.print("\n[bold]Cấu hình hiện tại:[/bold]")
        console.print(f"  Model: {current_model}")
        console.print(f"  Language: {current_lang}")
        console.print(f"  Show suggestions: {current_show_sugg}")
        console.print(f"  API key: {masked_api}")
        console.print(f"  Aliases: {aliases if aliases else '(không có)'}\n")
    
    def _configure(self):
        """Run configuration setup"""
        setup_configuration(self.config, self.os_type)
    
    def _set_api_key(self):
        """Set new API key"""
        new_key = input("Enter new API key: ").strip()
        if new_key:
            self.config.set_api_key(new_key)
            print_success("API key updated")
    
    def _set_model(self):
        """Set AI model"""
        console.print("Select model:")
        for i, m in enumerate(AVAILABLE_MODELS, 1):
            console.print(f"  {i}. {m}")
        
        choice = input("Choice (1-4): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(AVAILABLE_MODELS):
            selected_model = AVAILABLE_MODELS[int(choice) - 1]
            self.config.set_model(selected_model)
            print_success(f"Model set to {selected_model}")
    
    def _execute_alias(self, alias_name):
        """Execute alias if exists"""
        alias_cmd = self.alias_manager.get(alias_name)
        if alias_cmd:
            print_command(alias_cmd)
            if confirm("▶ Run this alias?"):
                execute_command(alias_cmd, capture_output=False)
            return True
        return False
    
    def _initialize_ai(self, api_key):
        """Initialize AI assistant"""
        model_name = self.config.get_model()
        self.ai = AIAssistant(api_key, model_name)
    
    def _start_chat_mode(self):
        """Start interactive chat mode"""
        chat = ChatMode(self.ai, self.os_type)
        chat.start()
    
    def _handle_query(self, query, run_directly=False):
        """Handle normal query mode"""
        show_suggestions = self.config.get_show_suggestions()
        
        print_thinking()
        
        try:
            command, options = self.ai.generate_command(
                query, self.os_type, show_suggestions
            )
            
            # Display command
            print_command(command)
            
            # Display suggestions if enabled
            if show_suggestions:
                print_options(options)
            
            # Copy to clipboard
            success, msg = copy_to_clipboard(command)
            console.print(f"[dim]{msg}[/dim]")
            
            # Execute if requested
            if run_directly or confirm("▶ Run this command?"):
                execute_command(command, capture_output=False)
        
        except Exception as e:
            print_error(str(e))
            sys.exit(1)