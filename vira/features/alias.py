"""
Alias management
"""
from ..config.manager import ConfigManager
from ..utils.console import print_success, print_warning, print_error, print_table


class AliasManager:
    """Manage command aliases"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
    
    def set(self, alias_str):
        """Set alias from string 'name=command'"""
        if "=" not in alias_str:
            print_error("Invalid format. Use: --set-alias name=command")
            return False
        
        name, command = alias_str.split("=", 1)
        name = name.strip()
        command = command.strip()
        
        self.config.set_alias(name, command)
        print_success(f"Alias '{name}' saved!")
        return True
    
    def remove(self, name):
        """Remove alias"""
        if self.config.remove_alias(name):
            print_success(f"Removed alias '{name}'")
            return True
        else:
            print_warning(f"Alias '{name}' not found")
            return False
    
    def list(self):
        """List all aliases"""
        aliases = self.config.list_aliases()
        
        if not aliases:
            print_warning("No aliases defined yet.")
            return
        
        rows = [[name, cmd] for name, cmd in aliases.items()]
        print_table("📘 Alias List", ["Name", "Command"], rows)
    
    def get(self, name):
        """Get alias command"""
        return self.config.get_alias(name)
    
    def exists(self, name):
        """Check if alias exists"""
        return self.config.get_alias(name) is not None