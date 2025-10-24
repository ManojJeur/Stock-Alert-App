"""
WhatsApp Alert System for Pincode Stock Checker
Sends alerts via Twilio WhatsApp API when stock status changes
"""

import os
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

logger = logging.getLogger(__name__)

class WhatsAppAlert:
    """Handles WhatsApp alerts via Twilio"""
    
    def __init__(self):
        """Initialize Twilio client"""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.recipient_number = os.getenv('RECIPIENT_PHONE_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.from_number, self.recipient_number]):
            logger.warning("Twilio configuration incomplete. Alerts will be logged only.")
            self.client = None
        else:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Twilio client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.client = None
    
    def send_alert(self, message: str, product_name: str = None, pincode: str = None) -> bool:
        """
        Send WhatsApp alert
        
        Args:
            message: Alert message to send
            product_name: Name of the product (optional)
            pincode: Pincode (optional)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Format the message with emojis and details
            formatted_message = self._format_message(message, product_name, pincode)
            
            if self.client:
                # Send via Twilio WhatsApp
                message_obj = self.client.messages.create(
                    body=formatted_message,
                    from_=self.from_number,
                    to=self.recipient_number
                )
                logger.info(f"WhatsApp alert sent successfully: {message_obj.sid}")
                return True
            else:
                # Log to console if Twilio not configured
                logger.info(f"ALERT (WhatsApp not configured): {formatted_message}")
                return True
                
        except TwilioException as e:
            logger.error(f"Twilio error sending alert: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending WhatsApp alert: {e}")
            return False
    
    def _format_message(self, message: str, product_name: str = None, pincode: str = None) -> str:
        """Format the alert message with emojis and details"""
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the message
        formatted = f"🛒 *Stock Alert* - {timestamp}\n\n"
        
        if product_name:
            formatted += f"📦 *Product:* {product_name}\n"
        
        if pincode:
            formatted += f"📍 *Pincode:* {pincode}\n"
        
        formatted += f"\n{message}\n\n"
        formatted += "🔄 *Next check in 10 minutes*"
        
        return formatted
    
    def send_stock_alert(self, product_name: str, pincode: str, status: str, previous_status: str = None) -> bool:
        """
        Send stock status change alert
        
        Args:
            product_name: Name of the product
            pincode: Pincode
            status: Current stock status
            previous_status: Previous stock status (optional)
            
        Returns:
            bool: True if sent successfully
        """
        if status == "OOS":
            message = "🚨 *OUT OF STOCK* - Product is no longer available!"
        elif status == "Low":
            message = "⚠️ *LOW STOCK* - Only a few units remaining!"
        elif status == "Available" and previous_status in ["Low", "OOS"]:
            message = "✅ *BACK IN STOCK* - Product is now available again!"
        elif status == "Available":
            message = "✅ *IN STOCK* - Product is available!"
        else:
            message = f"📊 *Status Update* - Stock status: {status}"
        
        return self.send_alert(message, product_name, pincode)
    
    def send_error_alert(self, error_message: str, product_name: str = None, pincode: str = None) -> bool:
        """Send error alert"""
        message = f"❌ *Error* - {error_message}"
        return self.send_alert(message, product_name, pincode)
    
    def send_summary_alert(self, summary_data: dict) -> bool:
        """Send daily summary alert"""
        total_products = len(summary_data)
        oos_count = sum(1 for data in summary_data.values() if data.get('status') == 'OOS')
        low_count = sum(1 for data in summary_data.values() if data.get('status') == 'Low')
        available_count = sum(1 for data in summary_data.values() if data.get('status') == 'Available')
        
        message = f"""📊 *Daily Stock Summary*
        
📦 Total Products: {total_products}
✅ Available: {available_count}
⚠️ Low Stock: {low_count}
🚨 Out of Stock: {oos_count}

🔄 Next check in 10 minutes"""
        
        return self.send_alert(message)

# Global alert instance
alert_system = WhatsAppAlert()

def send_whatsapp_alert(message: str, product_name: str = None, pincode: str = None) -> bool:
    """Convenience function to send WhatsApp alert"""
    return alert_system.send_alert(message, product_name, pincode)

def send_stock_alert(product_name: str, pincode: str, status: str, previous_status: str = None) -> bool:
    """Convenience function to send stock alert"""
    return alert_system.send_stock_alert(product_name, pincode, status, previous_status)

def send_error_alert(error_message: str, product_name: str = None, pincode: str = None) -> bool:
    """Convenience function to send error alert"""
    return alert_system.send_error_alert(error_message, product_name, pincode)

if __name__ == "__main__":
    # Test the alert system
    print("Testing WhatsApp Alert System...")
    
    # Test basic alert
    send_whatsapp_alert("Test message from Pincode Stock Checker")
    
    # Test stock alert
    send_stock_alert("Test Product", "400001", "OOS", "Available")
    
    print("Test alerts sent!")
