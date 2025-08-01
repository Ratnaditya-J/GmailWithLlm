"""
GmailWithLLM - Deep email mining and LLM-powered insights
Main application entry point with secure credential handling.
"""

import sys
import atexit
from colorama import Fore, Style, init
from oauth_manager import OAuthManager
from gmail_client import GmailClient
from llm_client import LLMClient
from query_interface import QueryInterface

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class GmailWithLLM:
    """Main application class for GmailWithLLM."""
    
    def __init__(self):
        """Initialize application with security-first defaults."""
        self.oauth_manager = None
        self.gmail_client = None
        self.llm_client = None
        self.query_interface = None
        
        # Register cleanup function for secure exit
        atexit.register(self.cleanup)
    
    def run(self):
        """Main application workflow."""
        try:
            self._show_welcome()
            
            # Step 1: Gmail OAuth2 Authentication
            if not self._authenticate_gmail():
                return False
            
            # Step 2: LLM Authentication
            if not self._authenticate_llm():
                return False
            
            # Step 3: Start Interactive Interface
            self._start_interface()
            
            return True
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Application interrupted by user{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Application error: {str(e)}{Style.RESET_ALL}")
            return False
        finally:
            self.cleanup()
    
    def _show_welcome(self):
        """Display welcome message and security notice."""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🤖 Welcome to GmailWithLLM{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📧 Deep Email Mining & LLM-Powered Insights{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}🔒 Privacy-First Design:{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}Runtime-only credential collection{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}No data persistence to disk{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}Local email processing only{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}Automatic credential cleanup on exit{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}🎯 What you can do:{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}Ask natural language questions about your email history{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}Extract travel confirmations, receipts, recommendations{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}Analyze communication patterns and trends{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}Search and summarize email content with AI{Style.RESET_ALL}")
        
        print(f"\n{Fore.RED}⚠️  Security Notice:{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}You will be asked to authenticate with Gmail (OAuth2){Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}You will need to provide your LLM API key{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}No credentials will be saved to disk{Style.RESET_ALL}")
        print(f"   • {Fore.WHITE}All data is processed locally and securely{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def _authenticate_gmail(self) -> bool:
        """Authenticate with Gmail using OAuth2."""
        try:
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📧 Step 1: Gmail Authentication{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            
            self.oauth_manager = OAuthManager()
            credentials = self.oauth_manager.authenticate()
            
            if not credentials:
                print(f"{Fore.RED}❌ Gmail authentication failed{Style.RESET_ALL}")
                return False
            
            # Initialize Gmail client
            self.gmail_client = GmailClient(credentials)
            
            print(f"{Fore.GREEN}✅ Gmail authentication successful!{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Gmail authentication error: {str(e)}{Style.RESET_ALL}")
            return False
    
    def _authenticate_llm(self) -> bool:
        """Authenticate with LLM provider."""
        try:
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}🤖 Step 2: LLM Authentication{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            
            self.llm_client = LLMClient()
            
            if not self.llm_client.authenticate("openai"):
                print(f"{Fore.RED}❌ LLM authentication failed{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.GREEN}✅ LLM authentication successful!{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ LLM authentication error: {str(e)}{Style.RESET_ALL}")
            return False
    
    def _start_interface(self):
        """Start the interactive query interface."""
        try:
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}🚀 Step 3: Starting Interactive Interface{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            
            self.query_interface = QueryInterface(self.gmail_client, self.llm_client)
            self.query_interface.start()
            
        except Exception as e:
            print(f"{Fore.RED}❌ Interface error: {str(e)}{Style.RESET_ALL}")
    
    def cleanup(self):
        """Clean up all resources and credentials."""
        print(f"\n{Fore.YELLOW}🧹 Cleaning up application resources...{Style.RESET_ALL}")
        
        try:
            if self.query_interface:
                self.query_interface.cleanup()
            
            if self.llm_client:
                self.llm_client.cleanup()
            
            if self.gmail_client:
                self.gmail_client.cleanup()
            
            if self.oauth_manager:
                self.oauth_manager.cleanup()
            
            print(f"{Fore.GREEN}✅ All resources cleaned up securely{Style.RESET_ALL}")
            print(f"{Fore.GREEN}🔒 No credentials or email data persisted{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Cleanup warning: {str(e)}{Style.RESET_ALL}")

def main():
    """Main entry point."""
    try:
        app = GmailWithLLM()
        success = app.run()
        
        if success:
            print(f"\n{Fore.GREEN}✅ GmailWithLLM completed successfully{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️  GmailWithLLM exited early{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
