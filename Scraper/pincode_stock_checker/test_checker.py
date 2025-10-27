"""
Test script for Pincode Stock Checker
"""

import json
import logging
from checker import PincodeStockChecker
from alert import send_whatsapp_alert, send_stock_alert

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_alert_system():
    """Test the alert system"""
    print("Testing alert system...")
    
    # Test basic alert
    send_whatsapp_alert("Test message from Pincode Stock Checker")
    
    # Test stock alerts
    send_stock_alert("Test Product", "400001", "OOS", "Available")
    send_stock_alert("Test Product", "400002", "Low", "Available")
    send_stock_alert("Test Product", "400003", "Available", "OOS")
    
    print("Alert tests completed!")

def test_platform_adapters():
    """Test platform adapters"""
    print("Testing platform adapters...")
    
    from platform_adapters import get_platform_adapter, detect_platform_from_url
    
    # Test platform detection
    test_urls = [
        "https://blinkit.com/products/test",
        "https://www.swiggy.com/instamart/item/test",
        "https://zepto.com/products/test"
    ]
    
    for url in test_urls:
        platform = detect_platform_from_url(url)
        print(f"URL: {url} -> Platform: {platform}")
    
    # Test adapters
    try:
        blinkit_adapter = get_platform_adapter("blinkit")
        print("Blinkit adapter created successfully")
    except Exception as e:
        print(f"Error creating Blinkit adapter: {e}")
    
    try:
        swiggy_adapter = get_platform_adapter("swiggy")
        print("Swiggy adapter created successfully")
    except Exception as e:
        print(f"Error creating Swiggy adapter: {e}")

def test_checker():
    """Test the main checker"""
    print("Testing main checker...")
    
    try:
        checker = PincodeStockChecker("config.json")
        print("Checker initialized successfully")
        
        # Test configuration loading
        print(f"Pincodes: {checker.config.get('pincodes', [])}")
        print(f"Products: {list(checker.config.get('products', {}).keys())}")
        
        # Test single run
        print("Running single check...")
        checker.run_once()
        print("Single check completed!")
        
    except Exception as e:
        print(f"Error testing checker: {e}")

def create_test_config():
    """Create a test configuration"""
    test_config = {
        "pincodes": ["400001", "400002"],
        "products": {
            "Test Product 1": {
                "url": "https://blinkit.com/products/test-product-1",
                "platform": "blinkit"
            },
            "Test Product 2": {
                "url": "https://www.swiggy.com/instamart/item/test",
                "platform": "swiggy"
            }
        },
        "alert_settings": {
            "send_alerts": True,
            "alert_on_status_change": True,
            "alert_on_low_stock": True,
            "alert_on_oos": True,
            "alert_on_back_in_stock": True,
            "send_daily_summary": False
        }
    }
    
    with open("test_config.json", "w") as f:
        json.dump(test_config, f, indent=4)
    
    print("Test configuration created: test_config.json")

if __name__ == "__main__":
    print("Pincode Stock Checker - Test Suite")
    print("=" * 50)
    
    # Create test config
    create_test_config()
    
    # Test alert system
    test_alert_system()
    print()
    
    # Test platform adapters
    test_platform_adapters()
    print()
    
    # Test main checker
    test_checker()
    print()
    
    print("All tests completed!")
