"""
Simple Swiggy Instamart parser that focuses on basic availability detection
"""

import requests
from bs4 import BeautifulSoup
import re
import time

def check_swiggy_availability(url):
    """Simple function to check if a Swiggy product is available or not"""
    print(f"Checking: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get all text content
            all_text = soup.get_text().lower()
            
            # Simple availability detection
            unavailable_indicators = [
                'out of stock', 'not available', 'unavailable', 'sold out',
                'currently unavailable', 'not in stock', 'out of stock',
                'unavailable', 'sold out', 'try again', 'error'
            ]
            
            available_indicators = [
                'add to cart', 'buy now', 'order now', 'available',
                'in stock', 'add', 'buy', 'order'
            ]
            
            # Check for unavailable indicators
            unavailable_found = []
            for indicator in unavailable_indicators:
                if indicator in all_text:
                    unavailable_found.append(indicator)
            
            # Check for available indicators
            available_found = []
            for indicator in available_indicators:
                if indicator in all_text:
                    available_found.append(indicator)
            
            # Determine availability
            if unavailable_found:
                availability = "Out of Stock"
                stock_status = "Unavailable"
                print(f"  Unavailable indicators found: {unavailable_found}")
            elif available_found:
                availability = "Available"
                stock_status = "In Stock"
                print(f"  Available indicators found: {available_found}")
            else:
                availability = "Unknown"
                stock_status = "Unknown"
                print("  No clear availability indicators found")
            
            # Try to extract product name from title or any text
            title = soup.find('title')
            product_name = title.get_text().strip() if title else "Unknown Product"
            
            # Try to find any price information
            price_pattern = r'₹\s*(\d+(?:\.\d{2})?)'
            prices = re.findall(price_pattern, all_text)
            current_price = float(prices[0]) if prices else None
            
            result = {
                'product_name': product_name,
                'current_price': current_price,
                'availability': availability,
                'stock_status': stock_status,
                'product_url': url,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"  Product: {result['product_name']}")
            print(f"  Price: Rs {result['current_price'] if result['current_price'] else 'N/A'}")
            print(f"  Availability: {result['availability']}")
            print(f"  Stock Status: {result['stock_status']}")
            
            return result
            
        else:
            print(f"Failed to fetch: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_swiggy_urls():
    """Test with sample Swiggy URLs"""
    urls = [
        "https://www.swiggy.com/instamart/item/0IFZHN76PS"
    ]
    
    for url in urls:
        result = check_swiggy_availability(url)
        print("-" * 50)

if __name__ == "__main__":
    test_swiggy_urls()
