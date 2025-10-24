"""
Example usage of Blinkit Product Scraper
"""

from scraper import BlinkitScraper
import time

def example_single_scrape():
    """Example: Run a single scraping session"""
    print("🔍 Example: Single Scraping Session")
    print("=" * 40)
    
    # Initialize scraper
    scraper = BlinkitScraper()
    
    # Check database connection
    if not scraper.test_connection():
        print("❌ Database connection failed!")
        return
    
    # Run scraping
    print("Starting scraping session...")
    stats = scraper.scrape_all_products()
    
    print(f"Scraping completed!")
    print(f"Total processed: {stats['total_processed']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")

def example_database_stats():
    """Example: Get database statistics"""
    print("📊 Example: Database Statistics")
    print("=" * 40)
    
    scraper = BlinkitScraper()
    stats = scraper.get_database_stats()
    
    print("Database Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

def example_single_product():
    """Example: Scrape a single product"""
    print("🛍️ Example: Single Product Scraping")
    print("=" * 40)
    
    scraper = BlinkitScraper()
    
    # Example URL (replace with actual Blinkit URL)
    test_url = "https://blinkit.com/products/amul-butter-500g"
    
    print(f"Scraping single product: {test_url}")
    success = scraper.scrape_single_product(test_url)
    
    if success:
        print("✅ Product scraped successfully!")
    else:
        print("❌ Failed to scrape product")

def example_scheduled_scraping():
    """Example: Start scheduled scraping"""
    print("⏰ Example: Scheduled Scraping")
    print("=" * 40)
    print("This would start automatic scraping every 30 minutes")
    print("Press Ctrl+C to stop")
    
    # Uncomment the following lines to actually start scheduling
    # from scraper import setup_scheduler
    # setup_scheduler()

def main():
    """Run all examples"""
    print("🚀 Blinkit Scraper Examples")
    print("=" * 50)
    
    examples = [
        ("Database Statistics", example_database_stats),
        ("Single Product", example_single_product),
        ("Single Scrape Session", example_single_scrape),
        ("Scheduled Scraping", example_scheduled_scraping)
    ]
    
    for name, func in examples:
        print(f"\n📋 {name}")
        try:
            func()
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
        print("-" * 50)
        time.sleep(1)  # Small delay between examples
    
    print("\n✅ Examples completed!")
    print("\nTo run the scraper:")
    print("  python scraper.py scrape      # Single session")
    print("  python scraper.py schedule     # Automatic (30 min)")
    print("  python scraper.py stats        # Show statistics")
    print("  python scraper.py test         # Test connection")

if __name__ == "__main__":
    main()
