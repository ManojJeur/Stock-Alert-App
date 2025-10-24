"""
Pincode-wise Stock Checker
Monitors product availability across different pincodes and platforms
"""

import json
import time
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

from alert import send_stock_alert, send_error_alert, send_whatsapp_alert
from platform_adapters import get_platform_adapter, detect_platform_from_url

# Load environment variables
load_dotenv('config.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pincode_checker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PincodeStockChecker:
    """Main class for pincode-wise stock checking"""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize the checker with configuration"""
        self.config_file = config_file
        self.data_file = "data/last_status.json"
        self.check_interval = int(os.getenv('CHECK_INTERVAL_MINUTES', 10)) * 60  # Convert to seconds
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.retry_delay = int(os.getenv('RETRY_DELAY_SECONDS', 5))
        
        # Load configuration
        self.config = self._load_config()
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_file}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_file} not found. Creating default config.")
            return self._create_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """Create default configuration"""
        default_config = {
            "pincodes": ["400001", "400002", "400003", "400004"],
            "products": {
                "Amul Butter 500g": {
                    "url": "https://blinkit.com/products/amul-butter-500g",
                    "platform": "blinkit"
                },
                "Maggie Noodles 8-Pack": {
                    "url": "https://blinkit.com/products/maggie-noodles-8-pack",
                    "platform": "blinkit"
                },
                "Coca Cola 600ml": {
                    "url": "https://www.swiggy.com/instamart/item/0IFZHN76PS",
                    "platform": "swiggy"
                }
            },
            "alert_settings": {
                "send_alerts": True,
                "alert_on_status_change": True,
                "alert_on_low_stock": True,
                "alert_on_oos": True,
                "alert_on_back_in_stock": True
            }
        }
        
        # Save default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        logger.info(f"Default configuration created at {self.config_file}")
        return default_config
    
    def _load_last_status(self) -> Dict:
        """Load last known status from file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logger.info("No previous status found. Starting fresh.")
            return {}
    
    def _save_last_status(self, status_data: Dict):
        """Save current status to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(status_data, f, indent=4)
            logger.debug("Status data saved successfully")
        except Exception as e:
            logger.error(f"Error saving status data: {e}")
    
    def _get_stock_status(self, product_url: str, pincode: str, platform: str = None) -> Tuple[str, str, Optional[float]]:
        """Get stock status for a product in a specific pincode"""
        try:
            # Detect platform if not specified
            if not platform:
                platform = detect_platform_from_url(product_url)
            
            if platform == 'unknown':
                logger.warning(f"Unknown platform for URL: {product_url}")
                return "Error", "Unknown Platform", None
            
            # Get platform adapter
            adapter = get_platform_adapter(platform)
            
            # Get stock status with retries
            for attempt in range(self.max_retries):
                try:
                    status, stock_level, price = adapter.get_stock_status(product_url, pincode)
                    logger.debug(f"Stock check attempt {attempt + 1}: {status} for pincode {pincode}")
                    return status, stock_level, price
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {product_url} in {pincode}: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                    else:
                        logger.error(f"All attempts failed for {product_url} in {pincode}")
                        return "Error", "Check Failed", None
            
        except Exception as e:
            logger.error(f"Error getting stock status for {product_url} in {pincode}: {e}")
            return "Error", "Error", None
    
    def _should_send_alert(self, product_name: str, pincode: str, current_status: str, 
                          previous_status: str, alert_settings: Dict) -> bool:
        """Determine if an alert should be sent"""
        if not alert_settings.get("send_alerts", True):
            return False
        
        # No previous status - don't alert on first check
        if not previous_status:
            return False
        
        # Status changed
        if current_status != previous_status:
            if current_status == "OOS" and alert_settings.get("alert_on_oos", True):
                return True
            elif current_status == "Low" and alert_settings.get("alert_on_low_stock", True):
                return True
            elif current_status == "Available" and previous_status in ["Low", "OOS"] and alert_settings.get("alert_on_back_in_stock", True):
                return True
            elif alert_settings.get("alert_on_status_change", True):
                return True
        
        return False
    
    def check_all_products(self):
        """Check stock status for all products across all pincodes"""
        logger.info("Starting stock check cycle")
        
        # Load previous status
        last_status = self._load_last_status()
        new_status = {}
        
        # Get configuration
        pincodes = self.config.get("pincodes", [])
        products = self.config.get("products", {})
        alert_settings = self.config.get("alert_settings", {})
        
        if not pincodes:
            logger.error("No pincodes configured")
            return
        
        if not products:
            logger.error("No products configured")
            return
        
        logger.info(f"Checking {len(products)} products across {len(pincodes)} pincodes")
        
        # Check each product
        for product_name, product_info in products.items():
            product_url = product_info.get("url")
            platform = product_info.get("platform")
            
            if not product_url:
                logger.warning(f"No URL configured for product: {product_name}")
                continue
            
            new_status[product_name] = {}
            
            # Check each pincode
            for pincode in pincodes:
                logger.info(f"Checking {product_name} in pincode {pincode}")
                
                # Get current stock status
                current_status, stock_level, price = self._get_stock_status(
                    product_url, pincode, platform
                )
                
                # Store current status
                new_status[product_name][pincode] = {
                    "status": current_status,
                    "stock_level": stock_level,
                    "price": price,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Get previous status
                previous_data = last_status.get(product_name, {}).get(pincode, {})
                previous_status = previous_data.get("status")
                
                # Check if alert should be sent
                if self._should_send_alert(product_name, pincode, current_status, 
                                         previous_status, alert_settings):
                    logger.info(f"Status changed for {product_name} in {pincode}: {previous_status} -> {current_status}")
                    
                    # Send alert
                    try:
                        send_stock_alert(product_name, pincode, current_status, previous_status)
                        logger.info(f"Alert sent for {product_name} in {pincode}")
                    except Exception as e:
                        logger.error(f"Failed to send alert for {product_name} in {pincode}: {e}")
                        send_error_alert(f"Failed to send alert: {e}", product_name, pincode)
                
                # Small delay between requests
                time.sleep(1)
        
        # Save new status
        self._save_last_status(new_status)
        
        # Send summary if configured
        if alert_settings.get("send_daily_summary", False):
            self._send_summary_alert(new_status)
        
        logger.info("Stock check cycle completed")
    
    def _send_summary_alert(self, status_data: Dict):
        """Send daily summary alert"""
        try:
            total_products = len(status_data)
            total_checks = sum(len(pincodes) for pincodes in status_data.values())
            
            oos_count = 0
            low_count = 0
            available_count = 0
            error_count = 0
            
            for product_data in status_data.values():
                for pincode_data in product_data.values():
                    status = pincode_data.get("status")
                    if status == "OOS":
                        oos_count += 1
                    elif status == "Low":
                        low_count += 1
                    elif status == "Available":
                        available_count += 1
                    elif status == "Error":
                        error_count += 1
            
            summary_message = f"""📊 *Stock Check Summary*
            
📦 Products: {total_products}
🔍 Total Checks: {total_checks}
✅ Available: {available_count}
⚠️ Low Stock: {low_count}
🚨 Out of Stock: {oos_count}
❌ Errors: {error_count}

🔄 Next check in {self.check_interval // 60} minutes"""
            
            send_whatsapp_alert(summary_message)
            logger.info("Summary alert sent")
            
        except Exception as e:
            logger.error(f"Error sending summary alert: {e}")
    
    def run_continuous(self):
        """Run the checker continuously"""
        logger.info("Starting continuous pincode stock checking")
        logger.info(f"Check interval: {self.check_interval // 60} minutes")
        
        try:
            while True:
                start_time = time.time()
                
                try:
                    self.check_all_products()
                except Exception as e:
                    logger.error(f"Error in stock check cycle: {e}")
                    send_error_alert(f"Stock check cycle failed: {e}")
                
                # Calculate sleep time
                elapsed_time = time.time() - start_time
                sleep_time = max(0, self.check_interval - elapsed_time)
                
                logger.info(f"Cycle completed in {elapsed_time:.2f}s. Sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logger.info("Stopping pincode stock checker")
        except Exception as e:
            logger.error(f"Fatal error in continuous mode: {e}")
            send_error_alert(f"Pincode stock checker crashed: {e}")
    
    def run_once(self):
        """Run the checker once"""
        logger.info("Running single stock check")
        try:
            self.check_all_products()
            logger.info("Single check completed")
        except Exception as e:
            logger.error(f"Error in single check: {e}")
            send_error_alert(f"Single check failed: {e}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pincode Stock Checker")
    parser.add_argument("--mode", choices=["once", "continuous"], default="once",
                       help="Run mode: once or continuous")
    parser.add_argument("--config", default="config.json",
                       help="Configuration file path")
    
    args = parser.parse_args()
    
    # Initialize checker
    checker = PincodeStockChecker(args.config)
    
    # Run based on mode
    if args.mode == "continuous":
        checker.run_continuous()
    else:
        checker.run_once()

if __name__ == "__main__":
    main()
