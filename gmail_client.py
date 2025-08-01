"""
Gmail Client for fetching and analyzing email data.
Handles Gmail API integration with privacy-first design.
"""

import base64
import email
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from colorama import Fore, Style, init
import html2text
from bs4 import BeautifulSoup

# Initialize colorama
init(autoreset=True)

class GmailClient:
    """Gmail API client for secure email data fetching and analysis."""
    
    def __init__(self, credentials: Credentials):
        """Initialize Gmail client with authenticated credentials."""
        self.credentials = credentials
        self.service = None
        self.user_email = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Gmail API."""
        try:
            print(f"{Fore.CYAN}📧 Connecting to Gmail API...{Style.RESET_ALL}")
            self.service = build('gmail', 'v1', credentials=self.credentials)
            
            # Get user profile to verify connection
            profile = self.service.users().getProfile(userId='me').execute()
            self.user_email = profile.get('emailAddress', 'Unknown')
            
            print(f"{Fore.GREEN}✅ Connected to Gmail: {self.user_email}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📊 Total messages: {profile.get('messagesTotal', 'Unknown')}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to connect to Gmail: {str(e)}{Style.RESET_ALL}")
            raise
    
    def search_emails(self, query: str = "", max_results: int = 100, 
                     date_range: Optional[Tuple[str, str]] = None) -> List[Dict[str, Any]]:
        """
        Search emails with optional query and date range.
        
        Args:
            query: Gmail search query (e.g., "from:friend@example.com")
            max_results: Maximum number of emails to fetch
            date_range: Tuple of (start_date, end_date) in YYYY/MM/DD format
            
        Returns:
            List of email dictionaries with metadata and content
        """
        try:
            print(f"{Fore.CYAN}🔍 Searching emails...{Style.RESET_ALL}")
            
            # Build search query
            search_query = query
            if date_range:
                start_date, end_date = date_range
                if start_date:
                    search_query += f" after:{start_date}"
                if end_date:
                    search_query += f" before:{end_date}"
            
            print(f"{Fore.YELLOW}📋 Query: {search_query or 'All emails'}{Style.RESET_ALL}")
            
            # Search for message IDs
            results = self.service.users().messages().list(
                userId='me',
                q=search_query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            print(f"{Fore.GREEN}📧 Found {len(messages)} emails{Style.RESET_ALL}")
            
            if not messages:
                return []
            
            # Fetch full email data
            emails = []
            for i, message in enumerate(messages):
                try:
                    print(f"{Fore.CYAN}📥 Fetching email {i+1}/{len(messages)}...{Style.RESET_ALL}", end='\r')
                    email_data = self._get_email_details(message['id'])
                    if email_data:
                        emails.append(email_data)
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠️  Skipped email {i+1}: {str(e)}{Style.RESET_ALL}")
                    continue
            
            print(f"{Fore.GREEN}✅ Successfully fetched {len(emails)} emails{Style.RESET_ALL}")
            return emails
            
        except Exception as e:
            print(f"{Fore.RED}❌ Email search failed: {str(e)}{Style.RESET_ALL}")
            return []
    
    def _get_email_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed email data for a specific message ID."""
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = {}
            for header in message['payload'].get('headers', []):
                headers[header['name'].lower()] = header['value']
            
            # Extract email content
            body = self._extract_email_body(message['payload'])
            
            # Parse date
            date_str = headers.get('date', '')
            try:
                # Parse email date (RFC 2822 format)
                parsed_date = email.utils.parsedate_to_datetime(date_str)
                formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_date = date_str
            
            return {
                'id': message_id,
                'thread_id': message.get('threadId'),
                'subject': headers.get('subject', 'No Subject'),
                'from': headers.get('from', 'Unknown Sender'),
                'to': headers.get('to', 'Unknown Recipient'),
                'date': formatted_date,
                'date_raw': date_str,
                'body': body,
                'snippet': message.get('snippet', ''),
                'labels': message.get('labelIds', []),
                'headers': headers
            }
            
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Failed to fetch email details: {str(e)}{Style.RESET_ALL}")
            return None
    
    def _extract_email_body(self, payload: Dict[str, Any]) -> str:
        """Extract readable text from email payload."""
        body = ""
        
        try:
            # Handle multipart emails
            if 'parts' in payload:
                for part in payload['parts']:
                    body += self._extract_email_body(part)
            else:
                # Single part email
                if payload.get('body', {}).get('data'):
                    data = payload['body']['data']
                    # Decode base64
                    decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    
                    # Handle HTML content
                    mime_type = payload.get('mimeType', '')
                    if 'html' in mime_type:
                        # Convert HTML to text
                        soup = BeautifulSoup(decoded, 'html.parser')
                        body += soup.get_text(separator=' ', strip=True)
                    else:
                        body += decoded
                        
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Failed to extract email body: {str(e)}{Style.RESET_ALL}")
            return ""
        
        return body.strip()
    
    def get_recent_emails(self, days: int = 30, max_results: int = 50) -> List[Dict[str, Any]]:
        """Get recent emails from the last N days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        date_range = (
            start_date.strftime('%Y/%m/%d'),
            end_date.strftime('%Y/%m/%d')
        )
        
        return self.search_emails(
            query="",
            max_results=max_results,
            date_range=date_range
        )
    
    def search_by_sender(self, sender: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search emails from a specific sender."""
        return self.search_emails(
            query=f"from:{sender}",
            max_results=max_results
        )
    
    def search_by_subject(self, subject_keywords: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search emails by subject keywords."""
        return self.search_emails(
            query=f"subject:{subject_keywords}",
            max_results=max_results
        )
    
    def search_by_content(self, content_keywords: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search emails by content keywords."""
        return self.search_emails(
            query=content_keywords,
            max_results=max_results
        )
    
    def get_email_statistics(self, emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate basic statistics from email data."""
        if not emails:
            return {}
        
        # Count by sender
        senders = {}
        subjects = []
        dates = []
        
        for email_data in emails:
            sender = email_data.get('from', 'Unknown')
            # Extract email address from "Name <email@domain.com>" format
            sender_match = re.search(r'<(.+?)>', sender)
            if sender_match:
                sender = sender_match.group(1)
            
            senders[sender] = senders.get(sender, 0) + 1
            subjects.append(email_data.get('subject', ''))
            dates.append(email_data.get('date', ''))
        
        # Top senders
        top_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_emails': len(emails),
            'unique_senders': len(senders),
            'top_senders': top_senders,
            'date_range': {
                'earliest': min(dates) if dates else None,
                'latest': max(dates) if dates else None
            }
        }
    
    def cleanup(self):
        """Clean up Gmail client resources."""
        print(f"{Fore.YELLOW}🧹 Cleaning up Gmail client...{Style.RESET_ALL}")
        self.service = None
        self.credentials = None
        print(f"{Fore.GREEN}✅ Gmail client cleaned up{Style.RESET_ALL}")
