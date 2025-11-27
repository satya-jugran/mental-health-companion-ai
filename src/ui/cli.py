"""
Enhanced CLI Interface for Mental Health Support Companion
Provides a clean, user-friendly command-line experience
"""
import os
from datetime import datetime

class CLI:
    """CLI Interface with formatting and menu support"""
    
    # ANSI color codes
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header():
        """Print the application header"""
        print(f"\n{CLI.HEADER}{CLI.BOLD}╔═══════════════════════════════════════════════════╗{CLI.END}")
        print(f"{CLI.HEADER}{CLI.BOLD}║   Mental Health Support Companion (ADK Powered)  ║{CLI.END}")
        print(f"{CLI.HEADER}{CLI.BOLD}╚═══════════════════════════════════════════════════╝{CLI.END}\n")
    
    @staticmethod
    def print_menu():
        """Print the main command menu"""
        print(f"{CLI.CYAN}{CLI.BOLD}Available Commands:{CLI.END}")
        print(f"  {CLI.GREEN}1.{CLI.END} {CLI.BOLD}mood{CLI.END}     - Log your current mood")
        print(f"  {CLI.GREEN}2.{CLI.END} {CLI.BOLD}patterns{CLI.END} - View your mood patterns and trends")
        print(f"  {CLI.GREEN}3.{CLI.END} {CLI.BOLD}support{CLI.END}  - Get coping strategies and advice")
        print(f"  {CLI.GREEN}4.{CLI.END} {CLI.BOLD}help{CLI.END}     - Get help or ask questions")
        print(f"  {CLI.GREEN}5.{CLI.END} {CLI.BOLD}menu{CLI.END}     - Show this menu again")
        print(f"  {CLI.RED}6.{CLI.END} {CLI.BOLD}exit{CLI.END}     - Exit the application\n")
    
    @staticmethod
    def print_welcome(user_name: str):
        """Print welcome message"""
        current_hour = datetime.now().hour
        greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"
        
        print(f"{CLI.BLUE}💙 {greeting}, {user_name}!{CLI.END}")
        print(f"{CLI.CYAN}I'm here to support you. How can I help today?{CLI.END}\n")
    
    @staticmethod
    def print_divider():
        """Print a visual divider"""
        print(f"{CLI.CYAN}{'─' * 60}{CLI.END}")
    
    @staticmethod
    def format_agent_response(agent_name: str, response: str) -> str:
        """Format agent responses with visual clarity"""
        icon_map = {
            "MoodTrackerAgent": "📝",
            "PatternAnalyzerAgent": "📊",
            "SupportAgent": "🤝",
            "CrisisMonitorAgent": "🆘",
            "OrchestratorAgent": "🎯"
        }
        icon = icon_map.get(agent_name, "💬")
        
        formatted = f"\n{CLI.BLUE}{icon} {CLI.BOLD}Companion:{CLI.END}\n"
        formatted += f"{response}\n"
        return formatted
    
    @staticmethod
    def get_input(prompt: str = "You") -> str:
        """Get user input with formatted prompt"""
        return input(f"\n{CLI.GREEN}{CLI.BOLD}{prompt}:{CLI.END} ").strip()
    
    @staticmethod
    def print_error(message: str):
        """Print error message"""
        print(f"\n{CLI.RED}❌ Error:{CLI.END} {message}\n")
    
    @staticmethod
    def print_success(message: str):
        """Print success message"""
        print(f"\n{CLI.GREEN}✓ {message}{CLI.END}\n")
    
    @staticmethod
    def print_info(message: str):
        """Print info message"""
        print(f"\n{CLI.CYAN}ℹ {message}{CLI.END}\n")
    
    @staticmethod
    def print_warning(message: str):
        """Print warning message"""
        print(f"\n{CLI.YELLOW}⚠ {message}{CLI.END}\n")
    
    @staticmethod
    def confirm_exit() -> bool:
        """Ask for exit confirmation"""
        response = input(f"\n{CLI.YELLOW}Are you sure you want to exit? (y/n):{CLI.END} ").strip().lower()
        return response in ['y', 'yes']
    
    @staticmethod
    def print_goodbye():
        """Print goodbye message"""
        print(f"\n{CLI.BLUE}💙 Thank you for using the Mental Health Support Companion.{CLI.END}")
        print(f"{CLI.CYAN}Take care, and remember: You're not alone.{CLI.END}\n")
    
    @staticmethod
    def show_quick_tips():
        """Show quick usage tips"""
        print(f"\n{CLI.CYAN}{CLI.BOLD}💡 Quick Tips:{CLI.END}")
        print(f"  • Type {CLI.GREEN}'mood'{CLI.END} to quickly log how you're feeling")
        print(f"  • Type {CLI.GREEN}'patterns'{CLI.END} to see your emotional trends")
        print(f"  • Type {CLI.GREEN}'menu'{CLI.END} anytime to see all commands")
        print(f"  • Just chat naturally - I'll understand what you need!\n")