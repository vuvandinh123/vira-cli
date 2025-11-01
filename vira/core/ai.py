"""
AI/Gemini integration
"""
import google.generativeai as genai
from vira.config.manager import ConfigManager

class AIAssistant:
    """Gemini AI assistant"""
    
    def __init__(self, api_key, model_name):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chat = None
        self.config = ConfigManager()
    
    def generate_command(self, query, os_type, show_options=True):
        """
        Generate shell command from natural language query
        Returns: (command: str, options: str)
        """
        language = self.config.get_language()
        lang_instruction = {
            "vi": "Trả lời bằng tiếng Việt.",
            "en": "Respond entirely in English."
        }.get(language.lower(), "Respond entirely in English.")

        prompt = f"""
You are an expert {os_type} terminal assistant.
{lang_instruction}

The user will give you a request.
You must respond in this exact format:

COMMAND:
<the one-line valid shell command only>

OPTIONS:
<optional list of 3–6 useful command-line flags and what they do, each on its own line like '-h : show help'>
If there are no relevant options, write 'OPTIONS: none'.

User: "{query}"
Response:
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip().replace("```", "").strip()

            cmd = ""
            options_text = ""

            if "OPTIONS:" in text:
                parts = text.split("OPTIONS:")
                cmd = parts[0].replace("COMMAND:", "").strip().split("\n")[0]
                options_text = parts[1].strip()
            else:
                cmd = text.split("\n")[0].replace("COMMAND:", "").strip()

            # Clean up command
            for token in ["```bash", "```shell", "`"]:
                cmd = cmd.replace(token, "")
            cmd = cmd.strip()

            return cmd, options_text

        except Exception as e:
            raise Exception(f"API Error: {e}")
    def analyze_and_fix_error(self, error_context, os_type):
        """
        Analyze command error and generate a fix.
        Specialized function for error recovery.
        
        Args:
            error_context: String containing error details (command, stderr, stdout, etc.)
            os_type: Operating system type
            language: Response language
        
        Returns:
            tuple: (fixed_command: str, explanation: str)
        """
        language = self.config.get_language()
        lang_instruction = {
            "vi": "Trả lời bằng tiếng Việt.",
            "en": "Respond entirely in English."
        }.get(language.lower(), "Respond entirely in English.")

        prompt = f"""
    You are an expert {os_type} terminal debugger.
    {lang_instruction}

    Analyze the error below and provide a fix.
    You must respond in this EXACT format:

    EXPLANATION:
    <Brief 1-2 sentence explanation of what went wrong>

    COMMAND:
    <The corrected command that should work>

    {error_context}

    Response:
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip().replace("```", "").strip()
            
            explanation = ""
            fixed_command = ""
            
            # Parse the structured response
            if "EXPLANATION:" in text and "COMMAND:" in text:
                parts = text.split("COMMAND:")
                if len(parts) == 2:
                    explanation = parts[0].replace("EXPLANATION:", "").strip()
                    fixed_command = parts[1].strip().split("\n")[0]
            else:
                # Fallback: treat entire response as command
                fixed_command = text.split("\n")[0].strip()
            
            # Clean up command
            for token in ["```bash", "```shell", "```sh", "`"]:
                fixed_command = fixed_command.replace(token, "")
            fixed_command = fixed_command.strip()
            
            return fixed_command, explanation
            
        except Exception as e:
            raise Exception(f"API Error: {e}")
    def start_chat(self):
        """Start interactive chat session"""
        self.chat = self.model.start_chat(history=[])
        return self.chat
    
    def send_message(self, message):
        """Send message in chat mode"""
        if not self.chat:
            self.start_chat()
        
        response = self.chat.send_message(message)
        return response.text.strip().replace("```", "").strip()