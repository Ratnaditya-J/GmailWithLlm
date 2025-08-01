"""
LLM Client for email analysis and insights.
Supports multiple LLM providers with privacy-first design.
"""

import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from colorama import Fore, Style, init
import getpass

# Initialize colorama
init(autoreset=True)

class LLMClient:
    """LLM client for analyzing email data and generating insights."""
    
    def __init__(self):
        """Initialize LLM client with secure credential handling."""
        self.client = None
        self.api_key = None
        self.model = "gpt-4"  # Default model
        
    def authenticate(self, provider: str = "openai") -> bool:
        """
        Authenticate with LLM provider using runtime credentials.
        
        Args:
            provider: LLM provider ("openai", "anthropic", etc.)
            
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            if provider.lower() == "openai":
                return self._authenticate_openai()
            else:
                print(f"{Fore.RED}❌ Unsupported LLM provider: {provider}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ LLM authentication failed: {str(e)}{Style.RESET_ALL}")
            return False
    
    def _authenticate_openai(self) -> bool:
        """Authenticate with OpenAI API."""
        print(f"{Fore.CYAN}🤖 OpenAI API Authentication{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔑 Please enter your OpenAI API key{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   (Get one at: https://platform.openai.com/api-keys){Style.RESET_ALL}")
        
        # Secure API key input
        api_key = getpass.getpass("OpenAI API Key: ").strip()
        
        if not api_key:
            print(f"{Fore.RED}❌ No API key provided{Style.RESET_ALL}")
            return False
        
        try:
            # Test API key with a simple request
            self.client = OpenAI(api_key=api_key)
            
            # Test with a minimal request
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            
            if response and response.choices:
                self.api_key = api_key
                print(f"{Fore.GREEN}✅ OpenAI API authentication successful!{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}❌ Invalid API response{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ OpenAI authentication failed: {str(e)}{Style.RESET_ALL}")
            if "api_key" in str(e).lower():
                print(f"{Fore.YELLOW}💡 Please check your API key and billing status{Style.RESET_ALL}")
            return False
    
    def analyze_emails(self, emails: List[Dict[str, Any]], query: str) -> str:
        """
        Analyze email data using LLM based on user query.
        
        Args:
            emails: List of email dictionaries
            query: User's natural language query
            
        Returns:
            LLM analysis response
        """
        if not self.client:
            return "❌ LLM client not authenticated. Please authenticate first."
        
        if not emails:
            return "❌ No email data provided for analysis."
        
        try:
            print(f"{Fore.CYAN}🤖 Analyzing emails with LLM...{Style.RESET_ALL}")
            
            # Prepare email data for LLM
            email_summary = self._prepare_email_data(emails)
            
            # Create analysis prompt
            prompt = self._create_analysis_prompt(email_summary, query)
            
            # Send to LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            if response and response.choices:
                result = response.choices[0].message.content
                print(f"{Fore.GREEN}✅ Analysis complete{Style.RESET_ALL}")
                return result
            else:
                return "❌ No response from LLM"
                
        except Exception as e:
            print(f"{Fore.RED}❌ LLM analysis failed: {str(e)}{Style.RESET_ALL}")
            return f"❌ Analysis failed: {str(e)}"
    
    def _prepare_email_data(self, emails: List[Dict[str, Any]]) -> str:
        """Prepare email data for LLM analysis."""
        email_summaries = []
        
        for i, email in enumerate(emails[:50]):  # Limit to 50 emails for token management
            summary = {
                "id": i + 1,
                "date": email.get('date', 'Unknown'),
                "from": email.get('from', 'Unknown'),
                "subject": email.get('subject', 'No Subject'),
                "snippet": email.get('snippet', '')[:200],  # Limit snippet length
                "body_preview": email.get('body', '')[:300]  # Limit body preview
            }
            email_summaries.append(summary)
        
        return json.dumps(email_summaries, indent=2)
    
    def _create_analysis_prompt(self, email_data: str, user_query: str) -> str:
        """Create analysis prompt for LLM."""
        return f"""
Please analyze the following email data and answer the user's query.

USER QUERY: {user_query}

EMAIL DATA:
{email_data}

Please provide a comprehensive analysis that directly addresses the user's query. Include:
1. Direct answer to the query
2. Relevant patterns or insights from the email data
3. Specific examples from the emails when applicable
4. Any recommendations or suggestions based on the analysis

Format your response in a clear, organized manner with appropriate headings and bullet points.
"""
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for email analysis."""
        return """You are an expert email analyst helping users extract insights from their personal email data. 

Your capabilities include:
- Analyzing email patterns and trends
- Extracting specific information (travel, receipts, recommendations, etc.)
- Identifying communication patterns and relationships
- Providing actionable insights and recommendations
- Summarizing email content and conversations

Guidelines:
- Be thorough but concise in your analysis
- Focus on actionable insights
- Respect user privacy (this is their personal email data)
- Provide specific examples when possible
- Use clear formatting with headings and bullet points
- If data is insufficient, clearly state limitations

Always prioritize accuracy and usefulness in your responses."""
    
    def summarize_emails(self, emails: List[Dict[str, Any]]) -> str:
        """Generate a general summary of email data."""
        return self.analyze_emails(
            emails, 
            "Please provide a comprehensive summary of these emails, including key patterns, important senders, main topics, and any notable insights."
        )
    
    def extract_content_type(self, emails: List[Dict[str, Any]], content_type: str) -> str:
        """Extract specific content types from emails."""
        query = f"Please extract and summarize all {content_type} from these emails. Provide specific details and organize the information clearly."
        return self.analyze_emails(emails, query)
    
    def find_patterns(self, emails: List[Dict[str, Any]]) -> str:
        """Find communication patterns in email data."""
        return self.analyze_emails(
            emails,
            "Analyze these emails for communication patterns, including frequency, timing, sender relationships, and any notable trends or insights."
        )
    
    def cleanup(self):
        """Clean up LLM client and credentials."""
        print(f"{Fore.YELLOW}🧹 Cleaning up LLM client...{Style.RESET_ALL}")
        if self.api_key:
            self.api_key = None
        self.client = None
        print(f"{Fore.GREEN}✅ LLM client cleaned up{Style.RESET_ALL}")
    
    def is_authenticated(self) -> bool:
        """Check if LLM client is authenticated."""
        return self.client is not None and self.api_key is not None
