import argparse
def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Vira - Your AI Command Line Assistant",
        epilog="Example: vira 'create a python script that prints hello world' --run",
    )
    parser = argparse.ArgumentParser(
        description="🤖 CLI Helper - AI-powered terminal assistant"
    )
    
    # Main arguments
    parser.add_argument("query", nargs="*", help="Your natural language query")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive chat mode")
    parser.add_argument("--run", action="store_true", help="Run command immediately")
    parser.add_argument("--config", action="store_true", help="Configure settings")
    parser.add_argument("--setting", action="store_true", help="Show current configuration")
    
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
    return args