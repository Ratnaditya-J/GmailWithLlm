# GmailWithLLM 📧🤖

**Deep email mining and LLM-powered insights for your personal Gmail history**

## 💡 Project Motivation

Your Gmail inbox contains **years of valuable personal data**—travel confirmations, receipts, recommendations from friends, work discussions, and countless insights buried in thousands of emails. Yet accessing this wealth of information remains frustratingly difficult.

Current email tools, including Google's own **Gemini integration with Gmail**, only scratch the surface:

### 🔍 **The Problem with Existing Solutions**

**Gmail + Gemini Integration:**
- ✅ Helps compose and reply to emails
- ✅ Summarizes recent conversations
- ✅ Basic search assistance
- ❌ **Limited to recent emails and simple queries**
- ❌ **No deep historical analysis across years of data**
- ❌ **Cannot extract and categorize specific content types**
- ❌ **No pattern recognition or trend analysis**
- ❌ **Lacks semantic search across your entire email history**

**Other Email Tools:**
- EmailAnalytics: Business metrics, not personal insights
- Boomerang: Scheduling and reminders only
- SaneBox: Email organization, not content analysis
- Enterprise tools: Team-focused, not personal email mining

### 🎯 **The GmailWithLLM Solution**

Imagine being able to ask your **entire email history** questions like:
- *"Find all my travel confirmations from the past 3 years and extract destinations"*
- *"What restaurants have friends recommended to me, and in which cities?"*
- *"Show me patterns in my apartment hunting emails and extract key criteria"*
- *"Analyze my work project discussions and identify recurring themes"*
- *"Extract all receipts and categorize my spending patterns"*
- *"Find emails about career opportunities and summarize the trends"*

**GmailWithLLM** fills the critical gap between basic email assistance and **deep personal data mining**, giving you the power to unlock insights from years of your digital communication history.

## 🔒 Privacy-First Design

- **🚫 Zero credential storage** - Gmail OAuth2 tokens collected at runtime only
- **🚫 No cloud processing** - All email analysis happens locally
- **🚫 No data persistence** - Email content never saved to disk
- **✅ Secure memory handling** - Automatic cleanup on exit
- **✅ OAuth2 authentication** - Industry-standard secure Gmail access

## ✨ Key Features

### 🔍 **Deep Email Mining**
- Search across years of email history
- Extract specific content types (receipts, travel, recommendations)
- Identify communication patterns and trends
- Analyze email metadata and relationships

### 🤖 **LLM-Powered Insights**
- Natural language queries about your email data
- AI-powered content summarization and analysis
- Semantic search across email content
- Custom insights based on your specific needs

### 🎛️ **Interactive Interface**
- Command-line interface for easy interaction
- Real-time email data fetching
- Customizable analysis queries
- Secure credential management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Gmail account with API access enabled
- OpenAI API key (or other supported LLM)

### Installation
```bash
git clone https://github.com/yourusername/GmailWithLLM.git
cd GmailWithLLM
pip install -r requirements.txt
```

### Setup Gmail API Access
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API
4. Create OAuth2 credentials (Desktop application)
5. Download the credentials JSON file
6. Place it in the project directory as `credentials.json`

### Usage
```bash
python main.py
```

The application will:
1. 🔐 Prompt for Gmail OAuth2 authentication (browser-based)
2. 🔑 Request your LLM API key (hidden input)
3. 📧 Connect to your Gmail account
4. 🤖 Enable natural language queries about your email data

## 🔧 Technical Architecture

### Core Components
- **`oauth_manager.py`** - Secure OAuth2 Gmail authentication
- **`gmail_client.py`** - Gmail API integration and email fetching
- **`llm_client.py`** - LLM integration for analysis and insights
- **`query_interface.py`** - Interactive CLI for user queries
- **`main.py`** - Application orchestration and workflow

### Security Features
- Runtime-only credential collection
- Secure token handling with automatic cleanup
- No persistent storage of email content or credentials
- Local processing only (no cloud data transmission)

## 🎯 Example Queries

- *"What are my most frequent email contacts from last year?"*
- *"Find all receipts and calculate my spending patterns"*
- *"Extract travel itineraries and booking confirmations"*
- *"Show me important work emails I might have missed"*
- *"Analyze my email response patterns and productivity"*
- *"Find recommendations for restaurants, books, or services"*

## 🔐 Security & Privacy

**GmailWithLLM** is designed with privacy as the top priority:

- **No data leaves your machine** except for LLM API calls (content only)
- **OAuth2 tokens are never saved** to disk or configuration files
- **Email content is processed in memory** and discarded after analysis
- **All credentials are collected at runtime** and cleaned up on exit
- **Open source and auditable** - verify the security yourself

## 🤝 Contributing

This project follows the same security-first principles as RedditWithLLM. Contributions welcome!

## 📄 License

MIT License - see LICENSE file for details

---

**⚠️ Important:** This application requires your Gmail OAuth2 consent and LLM API key at runtime. No credentials are ever stored permanently. Always verify the source code before running any application that accesses your personal data.
