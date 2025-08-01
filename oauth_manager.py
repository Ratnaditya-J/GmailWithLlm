"""
OAuth2 Manager for secure Gmail authentication.
Handles runtime-only credential collection with zero persistence.
"""

import os
import json
import pickle
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class OAuthManager:
    """Manages secure OAuth2 authentication for Gmail API access."""
    
    # Gmail API scopes - readonly access for security
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.metadata'
    ]
    
    def __init__(self):
        """Initialize OAuth manager with security-first defaults."""
        self.credentials: Optional[Credentials] = None
        self.credentials_file = 'credentials.json'
        
    def authenticate(self) -> Credentials:
        """
        Perform OAuth2 authentication with Gmail.
        Returns valid credentials for Gmail API access.
        """
        print(f"{Fore.CYAN}🔐 Gmail OAuth2 Authentication{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️  This will open your browser for Gmail authentication{Style.RESET_ALL}")
        
        # Check if credentials file exists
        if not os.path.exists(self.credentials_file):
            print(f"{Fore.RED}❌ Error: {self.credentials_file} not found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}📋 Please follow these steps:{Style.RESET_ALL}")
            print("   1. Go to https://console.cloud.google.com/")
            print("   2. Create a new project or select existing one")
            print("   3. Enable the Gmail API")
            print("   4. Create OAuth2 credentials (Desktop application)")
            print("   5. Download credentials.json to this directory")
            raise FileNotFoundError(f"Gmail API credentials file '{self.credentials_file}' not found")
        
        try:
            # Load credentials from file
            with open(self.credentials_file, 'r') as f:
                client_config = json.load(f)
            
            print(f"{Fore.GREEN}✅ Found credentials file{Style.RESET_ALL}")
            print(f"{Fore.CYAN}🌐 Opening browser for authentication...{Style.RESET_ALL}")
            
            # Create OAuth2 flow
            flow = InstalledAppFlow.from_client_config(
                client_config, 
                self.SCOPES
            )
            
            # Run local server for OAuth callback
            # This will open browser and handle the OAuth flow
            credentials = flow.run_local_server(
                port=0,  # Use random available port
                prompt='consent',  # Always show consent screen
                authorization_prompt_message='Please visit this URL to authorize the application: {url}',
                success_message='Authentication successful! You can close this window.',
                open_browser=True
            )
            
            if credentials and credentials.valid:
                self.credentials = credentials
                print(f"{Fore.GREEN}✅ Gmail authentication successful!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}📧 Connected to Gmail account{Style.RESET_ALL}")
                return credentials
            else:
                raise Exception("Authentication failed - invalid credentials")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Authentication failed: {str(e)}{Style.RESET_ALL}")
            raise
    
    def get_credentials(self) -> Optional[Credentials]:
        """Get current valid credentials."""
        return self.credentials
    
    def is_authenticated(self) -> bool:
        """Check if we have valid credentials."""
        return self.credentials is not None and self.credentials.valid
    
    def refresh_credentials(self) -> bool:
        """
        Refresh expired credentials if possible.
        Returns True if refresh successful, False otherwise.
        """
        if not self.credentials:
            return False
            
        try:
            if self.credentials.expired and self.credentials.refresh_token:
                print(f"{Fore.YELLOW}🔄 Refreshing expired credentials...{Style.RESET_ALL}")
                self.credentials.refresh(Request())
                print(f"{Fore.GREEN}✅ Credentials refreshed successfully{Style.RESET_ALL}")
                return True
            return self.credentials.valid
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to refresh credentials: {str(e)}{Style.RESET_ALL}")
            return False
    
    def cleanup(self):
        """
        Clean up credentials from memory.
        Called on application exit for security.
        """
        if self.credentials:
            print(f"{Fore.YELLOW}🧹 Cleaning up OAuth credentials...{Style.RESET_ALL}")
            self.credentials = None
            print(f"{Fore.GREEN}✅ Credentials cleaned from memory{Style.RESET_ALL}")
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get basic user information for verification.
        Returns email address and other safe metadata.
        """
        if not self.is_authenticated():
            return {}
        
        try:
            # Extract user email from token info if available
            if hasattr(self.credentials, 'id_token') and self.credentials.id_token:
                # This would require additional token parsing
                # For now, return basic info
                return {
                    "authenticated": True,
                    "scopes": self.SCOPES,
                    "valid": self.credentials.valid
                }
            else:
                return {
                    "authenticated": True,
                    "scopes": self.SCOPES,
                    "valid": self.credentials.valid
                }
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Could not retrieve user info: {str(e)}{Style.RESET_ALL}")
            return {"authenticated": True, "valid": self.credentials.valid}
