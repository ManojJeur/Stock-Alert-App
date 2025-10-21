# Stock Alert Dashboard Configuration

## Setup Instructions

1. Copy this file to `.env` in the alerts directory
2. Fill in your actual Twilio credentials
3. Update WhatsApp numbers with your actual numbers

## Required Environment Variables

```bash
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
YOUR_WHATSAPP_NUMBER=whatsapp:+1234567890

# Backend API Configuration
API_URL=http://localhost:8000
DATABASE_URL=sqlite:///stock_alerts.db

# Scraper Configuration
SCRAPER_INTERVAL=300
MAX_RETRIES=3
TIMEOUT=30

# Alert Configuration
ENABLE_WHATSAPP_ALERTS=true
ENABLE_EMAIL_ALERTS=false
ALERT_COOLDOWN=3600

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
```

## Getting Twilio Credentials

1. Sign up at https://www.twilio.com/
2. Get your Account SID and Auth Token from the dashboard
3. Set up WhatsApp Sandbox for testing
4. Use the sandbox number format: whatsapp:+14155238886

## Usage

1. Start the backend: `cd Backend && python main.py`
2. Run the scraper: `cd Scraper && python scraper.py`
3. Test WhatsApp: `cd alerts && python send_whatsapp.py`
