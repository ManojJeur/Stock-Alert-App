"""
Demo scraper with mock data to show Firebase integration
"""

import time
import random
from datetime import datetime
from scraper import SwiggyInstamartScraper

def create_mock_product_data(url: str) -> dict:
    """Create mock product data for demonstration"""
    products = [
        {
            "name": "Amul Butter 500g",
            "current_price": 285.0,
            "old_price": 310.0,
            "availability": "Available",
            "stock_status": "In Stock"
        },
        {
            "name": "Maggi Noodles 2-Minute Masala",
            "current_price": 12.0,
            "old_price": 15.0,
            "availability": "Available", 
            "stock_status": "Limited Stock"
        },
        {
            "name": "Coca Cola 600ml",
            "current_price": 35.0,
            "old_price": None,
            "availability": "Out of Stock",
            "stock_status": "Out of Stock"
        }
    ]
    
    # Select a random product or cycle through them
    product = random.choice(products)
    
    return {
        "product_name": product["name"],
        "current_price": product["current_price"],
        "old_price": product["old_price"],
        "availability": product["availability"],
        "stock_status": product["stock_status"],
        "product_url": url,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def demo_scraper():
    """Run demo scraper with mock data"""
    print("Swiggy Instamart Scraper Demo with Firebase")
    print("=" * 50)
    
    # Initialize scraper
    scraper = SwiggyInstamartScraper()
    
    # Test database connection
    if not scraper.test_connection():
        print("Database connection failed!")
        return
    
    print("Firebase connection successful!")
    
    # Get sample URLs
    urls = scraper.load_urls()
    if not urls:
        print("No URLs found in urls.txt")
        return
    
    print(f"Found {len(urls)} URLs to process")
    
    # Process each URL with mock data
    for i, url in enumerate(urls, 1):
        print(f"\nProcessing product {i}/{len(urls)}: {url}")
        
        # Create mock data
        mock_data = create_mock_product_data(url)
        print(f"   Product: {mock_data['product_name']}")
        print(f"   Price: Rs {mock_data['current_price']}")
        print(f"   Availability: {mock_data['availability']}")
        print(f"   Stock: {mock_data['stock_status']}")
        
        # Store in Firebase
        from db import get_db_connection
        with get_db_connection() as db:
            if db.insert_or_update_product(mock_data):
                print("   Stored in Firebase successfully!")
            else:
                print("   Failed to store in Firebase")
        
        # Small delay between requests
        time.sleep(1)
    
    # Show final statistics
    print("\nFinal Statistics:")
    stats = scraper.get_database_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\nDemo completed successfully!")
    print("\nTo view your data in Firebase:")
    print("1. Go to Firebase Console")
    print("2. Navigate to Firestore Database")
    print("3. Check the 'product_data' collection")

if __name__ == "__main__":
    demo_scraper()
