"""
Main Blinkit Product Scraper
Scrapes product data from Blinkit and stores in PostgreSQL database
"""

import logging
import time
import schedule
from typing import List, Dict, Any
from datetime import datetime

from db import get_db_connection, FirebaseManager
from utils import SwiggyInstamartParser, load_urls_from_file, validate_urls
from config import LOG_FORMAT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SwiggyInstamartScraper:
    """Main scraper class for Swiggy Instamart products"""
    
    def __init__(self, urls_file: str = "urls.txt"):
        self.urls_file = urls_file
        self.parser = SwiggyInstamartParser()
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'updated': 0,
            'new': 0
        }
    
    def load_urls(self) -> List[str]:
        """Load and validate URLs from file"""
        try:
            urls = load_urls_from_file(self.urls_file)
            valid_urls = validate_urls(urls)
            logger.info(f"Loaded {len(valid_urls)} valid URLs for scraping")
            return valid_urls
        except Exception as e:
            logger.error(f"Error loading URLs: {e}")
            return []
    
    def scrape_single_product(self, url: str) -> bool:
        """
        Scrape a single product and store in database
        
        Args:
            url: Product URL to scrape
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Scraping product: {url}")
            
            # Parse product data
            product_data = self.parser.parse_product_page(url)
            if not product_data:
                logger.warning(f"Failed to parse product data from: {url}")
                self.stats['failed'] += 1
                return False
            
            # Store in database
            with get_db_connection() as db:
                if db.insert_or_update_product(product_data):
                    logger.info(f"Successfully stored product: {product_data.get('product_name', 'Unknown')}")
                    self.stats['successful'] += 1
                    return True
                else:
                    logger.error(f"Failed to store product in database: {url}")
                    self.stats['failed'] += 1
                    return False
                    
        except Exception as e:
            logger.error(f"Error scraping product {url}: {e}")
            self.stats['failed'] += 1
            return False
    
    def scrape_all_products(self) -> Dict[str, int]:
        """
        Scrape all products from URLs file
        
        Returns:
            Dictionary with scraping statistics
        """
        logger.info("Starting product scraping session")
        start_time = time.time()
        
        # Reset stats
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'updated': 0,
            'new': 0
        }
        
        # Load URLs
        urls = self.load_urls()
        if not urls:
            logger.error("No valid URLs found to scrape")
            return self.stats
        
        logger.info(f"Starting to scrape {len(urls)} products")
        
        # Process each URL
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing product {i}/{len(urls)}: {url}")
            self.scrape_single_product(url)
            self.stats['total_processed'] += 1
            
            # Add delay between requests to be respectful
            if i < len(urls):  # Don't delay after the last request
                time.sleep(2)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Log final statistics
        logger.info("=" * 50)
        logger.info("SCRAPING SESSION COMPLETED")
        logger.info("=" * 50)
        logger.info(f"Total products processed: {self.stats['total_processed']}")
        logger.info(f"Successfully scraped: {self.stats['successful']}")
        logger.info(f"Failed to scrape: {self.stats['failed']}")
        logger.info(f"Execution time: {execution_time:.2f} seconds")
        logger.info(f"Average time per product: {execution_time/len(urls):.2f} seconds")
        logger.info("=" * 50)
        
        return self.stats
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get current database statistics"""
        try:
            with get_db_connection() as db:
                total_products = db.get_products_count()
                all_products = db.get_all_products()
                
                # Calculate availability stats
                available_count = sum(1 for p in all_products if p.get('availability') == 'Available')
                out_of_stock_count = sum(1 for p in all_products if p.get('availability') == 'Out of Stock')
                
                return {
                    'total_products': total_products,
                    'available': available_count,
                    'out_of_stock': out_of_stock_count,
                    'last_updated': max([p.get('timestamp') for p in all_products]) if all_products else None
                }
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with get_db_connection() as db:
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False


def run_scheduled_scrape():
    """Function to run scheduled scraping"""
    logger.info("Starting scheduled scraping run")
    scraper = SwiggyInstamartScraper()
    stats = scraper.scrape_all_products()
    logger.info(f"Scheduled scraping completed with stats: {stats}")


def setup_scheduler():
    """Setup the scheduler to run scraping every 30 minutes"""
    logger.info("Setting up scheduler for automatic scraping every 30 minutes")
    schedule.every(30).minutes.do(run_scheduled_scrape)
    
    # Run initial scrape
    logger.info("Running initial scrape...")
    run_scheduled_scrape()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def main():
    """Main function to run the scraper"""
    logger.info("Swiggy Instamart Product Scraper started")
    
    # Initialize scraper
    scraper = SwiggyInstamartScraper()
    
    # Test database connection
    if not scraper.test_connection():
        logger.error("Database connection failed. Please check your database configuration.")
        return
    
    # Get command line arguments or run interactively
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "scrape":
            # Run single scraping session
            logger.info("Running single scraping session")
            stats = scraper.scrape_all_products()
            print(f"Scraping completed. Stats: {stats}")
            
        elif command == "schedule":
            # Run with scheduler
            logger.info("Starting scheduled scraping")
            setup_scheduler()
            
        elif command == "stats":
            # Show database statistics
            stats = scraper.get_database_stats()
            print("Database Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
                
        elif command == "test":
            # Test database connection
            if scraper.test_connection():
                print("Database connection test: PASSED")
            else:
                print("Database connection test: FAILED")
        else:
            print("Unknown command. Use: scrape, schedule, stats, or test")
    else:
        # Interactive mode
        print("Swiggy Instamart Product Scraper")
        print("1. Run single scraping session")
        print("2. Start scheduled scraping (every 30 minutes)")
        print("3. Show database statistics")
        print("4. Test database connection")
        print("5. Exit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == "1":
                    stats = scraper.scrape_all_products()
                    print(f"Scraping completed. Stats: {stats}")
                    
                elif choice == "2":
                    print("Starting scheduled scraping (Ctrl+C to stop)...")
                    setup_scheduler()
                    
                elif choice == "3":
                    stats = scraper.get_database_stats()
                    print("Database Statistics:")
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                        
                elif choice == "4":
                    if scraper.test_connection():
                        print("Database connection test: PASSED")
                    else:
                        print("Database connection test: FAILED")
                        
                elif choice == "5":
                    print("Goodbye!")
                    break
                    
                else:
                    print("Invalid choice. Please enter 1-5.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
