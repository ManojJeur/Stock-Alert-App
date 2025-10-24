"""
Demo script for Pincode Stock Checker
Shows how to use the system with sample data
"""

import json
import time
from datetime import datetime
from checker import PincodeStockChecker
from alert import send_whatsapp_alert, send_stock_alert

def create_demo_config():
    """Create a demo configuration with sample data"""
    demo_config = {
        "pincodes": ["400001", "400002", "400003"],
        "products": {
            "Demo Product 1": {
                "url": "https://www.swiggy.com/instamart/item/0IFZHN76PS",
                "platform": "swiggy"
            },
            "Demo Product 2": {
                "url": "https://www.swiggy.com/instamart/item/OVACG3I2JD", 
                "platform": "swiggy"
            }
        },
        "alert_settings": {
            "send_alerts": True,
            "alert_on_status_change": True,
            "alert_on_low_stock": True,
            "alert_on_oos": True,
            "alert_on_back_in_stock": True,
            "send_daily_summary": True
        }
    }
    
    with open("demo_config.json", "w") as f:
        json.dump(demo_config, f, indent=4)
    
    print("Demo configuration created: demo_config.json")
    return demo_config

def simulate_stock_changes():
    """Simulate stock status changes for demo"""
    print("Simulating stock status changes...")
    
    # Simulate different scenarios
    scenarios = [
        ("Demo Product 1", "400001", "Available", None),
        ("Demo Product 1", "400002", "Low", "Available"),
        ("Demo Product 1", "400003", "OOS", "Available"),
        ("Demo Product 2", "400001", "Available", "OOS"),
        ("Demo Product 2", "400002", "Low", "Available"),
        ("Demo Product 2", "400003", "Available", "Low")
    ]
    
    for product_name, pincode, current_status, previous_status in scenarios:
        print(f"Simulating: {product_name} in {pincode}: {previous_status} -> {current_status}")
        
        # Send alert for status change
        if previous_status:
            send_stock_alert(product_name, pincode, current_status, previous_status)
            time.sleep(1)  # Small delay between alerts
    
    print("Stock change simulation completed!")

def demo_single_check():
    """Demo single stock check"""
    print("Running demo single check...")
    
    try:
        checker = PincodeStockChecker("demo_config.json")
        checker.run_once()
        print("Demo single check completed!")
    except Exception as e:
        print(f"Error in demo single check: {e}")

def demo_alert_system():
    """Demo the alert system"""
    print("Demo alert system...")
    
    # Test different alert types
    send_whatsapp_alert("Pincode Stock Checker Demo Started!")
    
    # Stock alerts
    send_stock_alert("Demo Product", "400001", "OOS", "Available")
    send_stock_alert("Demo Product", "400002", "Low", "Available") 
    send_stock_alert("Demo Product", "400003", "Available", "OOS")
    
    # Summary alert
    summary_data = {
        "Product 1": {
            "400001": {"status": "Available"},
            "400002": {"status": "Low"},
            "400003": {"status": "OOS"}
        },
        "Product 2": {
            "400001": {"status": "Available"},
            "400002": {"status": "Available"},
            "400003": {"status": "Low"}
        }
    }
    
    # Send summary
    total_products = len(summary_data)
    total_checks = sum(len(pincodes) for pincodes in summary_data.values())
    
    oos_count = sum(1 for product_data in summary_data.values() 
                   for pincode_data in product_data.values() 
                   if pincode_data.get("status") == "OOS")
    
    low_count = sum(1 for product_data in summary_data.values() 
                   for pincode_data in product_data.values() 
                   if pincode_data.get("status") == "Low")
    
    available_count = sum(1 for product_data in summary_data.values() 
                        for pincode_data in product_data.values() 
                        if pincode_data.get("status") == "Available")
    
    summary_message = f"""📊 *Demo Stock Summary*
    
📦 Products: {total_products}
🔍 Total Checks: {total_checks}
✅ Available: {available_count}
⚠️ Low Stock: {low_count}
🚨 Out of Stock: {oos_count}

🔄 This is a demo - no real monitoring active"""
    
    send_whatsapp_alert(summary_message)
    print("Demo alert system completed!")

def main():
    """Main demo function"""
    print("Pincode Stock Checker - Demo")
    print("=" * 50)
    
    # Create demo configuration
    demo_config = create_demo_config()
    print()
    
    # Demo alert system
    demo_alert_system()
    print()
    
    # Simulate stock changes
    simulate_stock_changes()
    print()
    
    # Demo single check
    demo_single_check()
    print()
    
    print("Demo completed!")
    print("\nTo run the actual checker:")
    print("1. Update config.env with your Twilio credentials")
    print("2. Update config.json with your products and pincodes")
    print("3. Run: python checker.py --mode once")
    print("4. Run: python checker.py --mode continuous")

if __name__ == "__main__":
    main()
