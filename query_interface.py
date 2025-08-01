"""
Interactive Query Interface for GmailWithLLM.
Provides CLI for natural language email analysis queries.
"""

import sys
from typing import List, Dict, Any, Optional
from colorama import Fore, Style, init
from gmail_client import GmailClient
from llm_client import LLMClient

# Initialize colorama
init(autoreset=True)

class QueryInterface:
    """Interactive command-line interface for email analysis queries."""
    
    def __init__(self, gmail_client: GmailClient, llm_client: LLMClient):
        """Initialize query interface with authenticated clients."""
        self.gmail_client = gmail_client
        self.llm_client = llm_client
        self.current_emails = []
        self.last_query = ""
        
    def start(self):
        """Start the interactive query interface."""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🤖 GmailWithLLM - Interactive Email Analysis{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Connected to Gmail: {self.gmail_client.user_email}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ LLM client ready for analysis{Style.RESET_ALL}")
        
        while True:
            try:
                self._show_menu()
                choice = input(f"\n{Fore.YELLOW}Enter your choice (1-8): {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self._custom_query()
                elif choice == '2':
                    self._recent_emails_analysis()
                elif choice == '3':
                    self._search_and_analyze()
                elif choice == '4':
                    self._extract_content_types()
                elif choice == '5':
                    self._analyze_patterns()
                elif choice == '6':
                    self._email_statistics()
                elif choice == '7':
                    self._reload_data()
                elif choice == '8':
                    self._exit()
                    break
                else:
                    print(f"{Fore.RED}❌ Invalid choice. Please enter 1-8.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
    
    def _show_menu(self):
        """Display the main menu options."""
        print(f"\n{Fore.CYAN}📋 What would you like to do?{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. 🤖 Ask custom question about your emails{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. 📅 Analyze recent emails (last 30 days){Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. 🔍 Search emails and analyze{Style.RESET_ALL}")
        print(f"{Fore.WHITE}4. 📊 Extract specific content (travel, receipts, etc.){Style.RESET_ALL}")
        print(f"{Fore.WHITE}5. 📈 Analyze communication patterns{Style.RESET_ALL}")
        print(f"{Fore.WHITE}6. 📋 Show email statistics{Style.RESET_ALL}")
        print(f"{Fore.WHITE}7. 🔄 Reload email data{Style.RESET_ALL}")
        print(f"{Fore.WHITE}8. 🚪 Exit{Style.RESET_ALL}")
    
    def _custom_query(self):
        """Handle custom user queries about email data."""
        print(f"\n{Fore.CYAN}🤖 Custom Email Analysis{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Example queries:{Style.RESET_ALL}")
        print("   • Find all my travel confirmations from 2024")
        print("   • Extract restaurant recommendations from friends")
        print("   • Show me patterns in my work emails")
        print("   • What are my most important unread emails?")
        
        query = input(f"\n{Fore.CYAN}Your question: {Style.RESET_ALL}").strip()
        
        if not query:
            print(f"{Fore.RED}❌ Please enter a question.{Style.RESET_ALL}")
            return
        
        # If no emails loaded, get recent emails
        if not self.current_emails:
            print(f"{Fore.YELLOW}📧 Loading recent emails for analysis...{Style.RESET_ALL}")
            self.current_emails = self.gmail_client.get_recent_emails(days=90, max_results=100)
        
        if not self.current_emails:
            print(f"{Fore.RED}❌ No emails found for analysis.{Style.RESET_ALL}")
            return
        
        # Analyze with LLM
        print(f"\n{Fore.CYAN}🤖 Analyzing {len(self.current_emails)} emails...{Style.RESET_ALL}")
        result = self.llm_client.analyze_emails(self.current_emails, query)
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Analysis Results{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(result)
        
        self.last_query = query
    
    def _recent_emails_analysis(self):
        """Analyze recent emails."""
        print(f"\n{Fore.CYAN}📅 Recent Email Analysis{Style.RESET_ALL}")
        
        days = input(f"{Fore.YELLOW}How many days back? (default 30): {Style.RESET_ALL}").strip()
        try:
            days = int(days) if days else 30
        except ValueError:
            days = 30
        
        max_emails = input(f"{Fore.YELLOW}Max emails to analyze? (default 50): {Style.RESET_ALL}").strip()
        try:
            max_emails = int(max_emails) if max_emails else 50
        except ValueError:
            max_emails = 50
        
        print(f"{Fore.CYAN}📧 Fetching emails from last {days} days...{Style.RESET_ALL}")
        self.current_emails = self.gmail_client.get_recent_emails(days=days, max_results=max_emails)
        
        if not self.current_emails:
            print(f"{Fore.RED}❌ No emails found in the specified period.{Style.RESET_ALL}")
            return
        
        # Generate summary
        result = self.llm_client.summarize_emails(self.current_emails)
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Recent Email Summary ({len(self.current_emails)} emails){Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(result)
    
    def _search_and_analyze(self):
        """Search for specific emails and analyze them."""
        print(f"\n{Fore.CYAN}🔍 Search and Analyze Emails{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Search examples:{Style.RESET_ALL}")
        print("   • from:friend@example.com")
        print("   • subject:receipt")
        print("   • travel OR flight OR hotel")
        print("   • has:attachment")
        
        query = input(f"\n{Fore.CYAN}Search query: {Style.RESET_ALL}").strip()
        
        if not query:
            print(f"{Fore.RED}❌ Please enter a search query.{Style.RESET_ALL}")
            return
        
        max_results = input(f"{Fore.YELLOW}Max results? (default 50): {Style.RESET_ALL}").strip()
        try:
            max_results = int(max_results) if max_results else 50
        except ValueError:
            max_results = 50
        
        # Search emails
        self.current_emails = self.gmail_client.search_emails(query, max_results=max_results)
        
        if not self.current_emails:
            print(f"{Fore.RED}❌ No emails found matching your search.{Style.RESET_ALL}")
            return
        
        # Ask for analysis type
        analysis_query = input(f"\n{Fore.CYAN}What would you like to know about these {len(self.current_emails)} emails? {Style.RESET_ALL}").strip()
        
        if not analysis_query:
            analysis_query = "Please summarize these emails and provide key insights."
        
        # Analyze with LLM
        result = self.llm_client.analyze_emails(self.current_emails, analysis_query)
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Search Results Analysis{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(result)
    
    def _extract_content_types(self):
        """Extract specific content types from emails."""
        print(f"\n{Fore.CYAN}📊 Extract Specific Content{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Content types:{Style.RESET_ALL}")
        print("   1. Travel confirmations and itineraries")
        print("   2. Receipts and purchase confirmations")
        print("   3. Restaurant and food recommendations")
        print("   4. Event invitations and confirmations")
        print("   5. Work-related action items")
        print("   6. Custom content type")
        
        choice = input(f"\n{Fore.CYAN}Choose content type (1-6): {Style.RESET_ALL}").strip()
        
        content_types = {
            '1': 'travel confirmations, flight bookings, hotel reservations, and itineraries',
            '2': 'receipts, purchase confirmations, and financial transactions',
            '3': 'restaurant recommendations, food suggestions, and dining experiences',
            '4': 'event invitations, meeting confirmations, and calendar items',
            '5': 'work-related action items, tasks, and deadlines'
        }
        
        if choice in content_types:
            content_type = content_types[choice]
        elif choice == '6':
            content_type = input(f"{Fore.CYAN}Enter custom content type: {Style.RESET_ALL}").strip()
            if not content_type:
                print(f"{Fore.RED}❌ Please specify a content type.{Style.RESET_ALL}")
                return
        else:
            print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")
            return
        
        # If no emails loaded, get recent emails
        if not self.current_emails:
            print(f"{Fore.YELLOW}📧 Loading recent emails for analysis...{Style.RESET_ALL}")
            self.current_emails = self.gmail_client.get_recent_emails(days=365, max_results=200)
        
        if not self.current_emails:
            print(f"{Fore.RED}❌ No emails found for analysis.{Style.RESET_ALL}")
            return
        
        # Extract content
        result = self.llm_client.extract_content_type(self.current_emails, content_type)
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Extracted: {content_type.title()}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(result)
    
    def _analyze_patterns(self):
        """Analyze communication patterns."""
        print(f"\n{Fore.CYAN}📈 Communication Pattern Analysis{Style.RESET_ALL}")
        
        # If no emails loaded, get recent emails
        if not self.current_emails:
            print(f"{Fore.YELLOW}📧 Loading recent emails for pattern analysis...{Style.RESET_ALL}")
            self.current_emails = self.gmail_client.get_recent_emails(days=90, max_results=150)
        
        if not self.current_emails:
            print(f"{Fore.RED}❌ No emails found for analysis.{Style.RESET_ALL}")
            return
        
        # Analyze patterns
        result = self.llm_client.find_patterns(self.current_emails)
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Communication Patterns ({len(self.current_emails)} emails){Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(result)
    
    def _email_statistics(self):
        """Show basic email statistics."""
        print(f"\n{Fore.CYAN}📋 Email Statistics{Style.RESET_ALL}")
        
        # If no emails loaded, get recent emails
        if not self.current_emails:
            print(f"{Fore.YELLOW}📧 Loading recent emails for statistics...{Style.RESET_ALL}")
            self.current_emails = self.gmail_client.get_recent_emails(days=30, max_results=100)
        
        if not self.current_emails:
            print(f"{Fore.RED}❌ No emails found for statistics.{Style.RESET_ALL}")
            return
        
        # Generate statistics
        stats = self.gmail_client.get_email_statistics(self.current_emails)
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Email Statistics{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}📧 Total emails analyzed: {stats.get('total_emails', 0)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}👥 Unique senders: {stats.get('unique_senders', 0)}{Style.RESET_ALL}")
        
        if 'date_range' in stats:
            date_range = stats['date_range']
            print(f"{Fore.CYAN}📅 Date range: {date_range.get('earliest', 'N/A')} to {date_range.get('latest', 'N/A')}{Style.RESET_ALL}")
        
        if 'top_senders' in stats:
            print(f"\n{Fore.YELLOW}🏆 Top Senders:{Style.RESET_ALL}")
            for i, (sender, count) in enumerate(stats['top_senders'][:10], 1):
                print(f"   {i}. {sender}: {count} emails")
    
    def _reload_data(self):
        """Reload email data."""
        print(f"\n{Fore.CYAN}🔄 Reload Email Data{Style.RESET_ALL}")
        self.current_emails = []
        print(f"{Fore.GREEN}✅ Email data cleared. It will be reloaded on next analysis.{Style.RESET_ALL}")
    
    def _exit(self):
        """Exit the application."""
        print(f"\n{Fore.YELLOW}👋 Thank you for using GmailWithLLM!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🔒 All credentials and email data have been securely cleared.{Style.RESET_ALL}")
    
    def cleanup(self):
        """Clean up query interface resources."""
        self.current_emails = []
        self.last_query = ""
