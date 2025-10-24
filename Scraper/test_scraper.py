"""
Test script for Blinkit Product Scraper
"""

import sys
import logging
from scraper import SwiggyInstamartScraper
from db import test_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database():
    """Test database connection"""
    print("Testing database connection...")
    if test_connection():
        print("Database connection: PASSED")
        return True
    else:
        print("Database connection: FAILED")
        return False

def test_scraper_initialization():
    """Test scraper initialization"""
    print("Testing scraper initialization...")
    try:
        scraper = SwiggyInstamartScraper()
        print("Scraper initialization: PASSED")
        return True
    except Exception as e:
        print(f"Scraper initialization: FAILED - {e}")
        return False

def test_url_loading():
    """Test URL loading functionality"""
    print("Testing URL loading...")
    try:
        scraper = SwiggyInstamartScraper()
        urls = scraper.load_urls()
        print(f"URL loading: PASSED - Loaded {len(urls)} URLs")
        return True
    except Exception as e:
        print(f"URL loading: FAILED - {e}")
        return False

def test_database_stats():
    """Test database statistics"""
    print("Testing database statistics...")
    try:
        scraper = SwiggyInstamartScraper()
        stats = scraper.get_database_stats()
        print(f"Database statistics: PASSED - {stats}")
        return True
    except Exception as e:
        print(f"Database statistics: FAILED - {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("Running Swiggy Instamart Scraper Tests")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database),
        ("Scraper Initialization", test_scraper_initialization),
        ("URL Loading", test_url_loading),
        ("Database Statistics", test_database_stats)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The scraper is ready to use.")
        return True
    else:
        print("Some tests failed. Please check the configuration.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
