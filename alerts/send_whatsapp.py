import os
from twilio.rest import Client
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class WhatsAppAlerts:
    def __init__(self):
        # Twilio credentials
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')  # Format: whatsapp:+1234567890
        
        # Your WhatsApp number (where alerts will be sent)
        self.to_number = os.getenv('YOUR_WHATSAPP_NUMBER')  # Format: whatsapp:+1234567890
        
        # Backend API URL
        self.api_url = os.getenv('API_URL', 'http://localhost:8000')
        
        # Initialize Twilio client
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            print("Warning: Twilio credentials not found. WhatsApp alerts disabled.")
    
    def send_whatsapp_message(self, message):
        """Send WhatsApp message using Twilio"""
        if not self.client or not self.to_number:
            print("WhatsApp not configured. Message would be:")
            print(message)
            return False
        
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=self.to_number
            )
            print(f"WhatsApp message sent successfully: {message_obj.sid}")
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
    
    def get_pending_alerts(self):
        """Get pending alerts from the backend API"""
        try:
            response = requests.get(f"{self.api_url}/alerts")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching alerts: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error connecting to API: {e}")
            return []
    
    def send_stock_alert(self, stock_symbol, current_price, alert_price, alert_type):
        """Send a formatted stock alert via WhatsApp"""
        emoji = "📈" if alert_type == "buy" else "📉"
        action = "BUY" if alert_type == "buy" else "SELL"
        
        message = f"""
{emoji} *STOCK ALERT* {emoji}

🏷️ *Stock:* {stock_symbol}
💰 *Current Price:* ${current_price:.2f}
🎯 *Alert Price:* ${alert_price:.2f}
⚡ *Action:* {action}
🕐 *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is an automated alert from your Stock Alert Dashboard.
        """.strip()
        
        return self.send_whatsapp_message(message)
    
    def send_test_message(self):
        """Send a test message to verify WhatsApp integration"""
        test_message = f"""
🧪 *TEST MESSAGE*

Your Stock Alert Dashboard WhatsApp integration is working correctly!

🕐 *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you received this message, your alerts are ready to go! 🚀
        """.strip()
        
        return self.send_whatsapp_message(test_message)
    
    def process_alerts(self):
        """Process all pending alerts and send via WhatsApp"""
        alerts = self.get_pending_alerts()
        
        if not alerts:
            print("No pending alerts found")
            return
        
        print(f"Processing {len(alerts)} alerts...")
        
        for alert in alerts:
            # Extract stock information from alert message
            message = alert.get('message', '')
            
            # Send the alert via WhatsApp
            success = self.send_whatsapp_message(message)
            
            if success:
                print(f"Alert sent successfully: {message[:50]}...")
            else:
                print(f"Failed to send alert: {message[:50]}...")
    
    def send_daily_summary(self):
        """Send a daily summary of stock performance"""
        try:
            # Get stocks data from API
            response = requests.get(f"{self.api_url}/stocks")
            if response.status_code != 200:
                print("Error fetching stocks data")
                return
            
            stocks = response.json()
            
            if not stocks:
                print("No stocks found for summary")
                return
            
            summary_message = f"""
📊 *DAILY STOCK SUMMARY*

🕐 *Date:* {datetime.now().strftime('%Y-%m-%d')}

"""
            
            for stock in stocks:
                symbol = stock['symbol']
                current_price = stock.get('current_price', 0)
                alert_price = stock['alert_price']
                alert_type = stock['alert_type']
                
                if current_price:
                    status = "✅" if (alert_type == "buy" and current_price <= alert_price) or (alert_type == "sell" and current_price >= alert_price) else "⏳"
                    summary_message += f"{status} *{symbol}:* ${current_price:.2f} (Target: ${alert_price:.2f})\n"
                else:
                    summary_message += f"❓ *{symbol}:* Price unavailable (Target: ${alert_price:.2f})\n"
            
            summary_message += "\n📱 *Stock Alert Dashboard*"
            
            self.send_whatsapp_message(summary_message)
            
        except Exception as e:
            print(f"Error sending daily summary: {e}")

def main():
    """Main function to test WhatsApp integration"""
    whatsapp = WhatsAppAlerts()
    
    print("Testing WhatsApp integration...")
    
    # Send test message
    whatsapp.send_test_message()
    
    # Process any pending alerts
    whatsapp.process_alerts()
    
    print("WhatsApp integration test completed!")

if __name__ == "__main__":
    main()
