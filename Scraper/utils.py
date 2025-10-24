"""
Unified utility functions for HTML fetching and parsing
Supports both traditional HTTP requests and Playwright stealth browsing
"""

import requests
import time
import logging
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Try to import config modules (may not exist in all setups)
try:
    from config import SCRAPING_CONFIG, REQUEST_HEADERS
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    SCRAPING_CONFIG = {
        "max_retries": 3,
        "retry_delay": 2,
        "request_timeout": 30
    }
    REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTMLFetcher:
    """Handles HTTP requests with retry logic and error handling"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(REQUEST_HEADERS)
        # Add some additional headers to mimic a real browser
        self.session.headers.update({
            'Referer': 'https://www.google.com/',
            'Origin': 'https://blinkit.com'
        })
    
    def fetch_page(self, url: str, max_retries: int = None) -> Optional[str]:
        """
        Fetch HTML content from URL with retry logic
        
        Args:
            url: URL to fetch
            max_retries: Maximum number of retry attempts
            
        Returns:
            HTML content as string or None if failed
        """
        if max_retries is None:
            max_retries = SCRAPING_CONFIG["max_retries"]
        
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Fetching page (attempt {attempt + 1}): {url}")
                
                response = self.session.get(
                    url, 
                    timeout=SCRAPING_CONFIG["request_timeout"],
                    allow_redirects=True
                )
                
                # Check if request was successful
                if response.status_code == 200:
                    logger.info(f"Successfully fetched page: {url}")
                    return response.text
                elif response.status_code == 404:
                    logger.warning(f"Page not found (404): {url}")
                    return None
                elif response.status_code == 403:
                    logger.warning(f"Access forbidden (403): {url}")
                    return None
                else:
                    logger.warning(f"Unexpected status code {response.status_code} for: {url}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout error (attempt {attempt + 1}): {url}")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error (attempt {attempt + 1}): {url}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request error (attempt {attempt + 1}): {e}")
            except Exception as e:
                logger.error(f"Unexpected error (attempt {attempt + 1}): {e}")
            
            # Wait before retry (exponential backoff)
            if attempt < max_retries:
                wait_time = SCRAPING_CONFIG["retry_delay"] * (2 ** attempt)
                logger.info(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        logger.error(f"Failed to fetch page after {max_retries + 1} attempts: {url}")
        return None
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and accessible"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and parsed.scheme in ['http', 'https']
        except Exception:
            return False


class SwiggyInstamartParser:
    """Parses Swiggy Instamart product pages to extract product information"""
    
    def __init__(self):
        self.fetcher = HTMLFetcher()
    
    def parse_product_page(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Parse Swiggy Instamart product page and extract product information
        
        Args:
            url: Swiggy Instamart product URL
            
        Returns:
            Dictionary with product data or None if parsing failed
        """
        try:
            # Fetch HTML content
            html_content = self.fetcher.fetch_page(url)
            if not html_content:
                return None
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract product information
            product_data = self._extract_product_data(soup, url)
            
            if product_data:
                logger.info(f"Successfully parsed product: {product_data.get('product_name', 'Unknown')}")
            else:
                logger.warning(f"Failed to extract product data from: {url}")
            
            return product_data
            
        except Exception as e:
            logger.error(f"Error parsing product page {url}: {e}")
            return None
    
    def _extract_product_data(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract product data from parsed HTML"""
        try:
            product_data = {
                'product_url': url,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Extract product name
            product_name = self._extract_product_name(soup)
            if not product_name:
                logger.warning("Could not extract product name")
                return None
            product_data['product_name'] = product_name
            
            # Extract prices
            current_price, old_price = self._extract_prices(soup)
            product_data['current_price'] = current_price
            product_data['old_price'] = old_price
            
            # Extract availability and stock status
            availability, stock_status = self._extract_availability(soup)
            product_data['availability'] = availability
            product_data['stock_status'] = stock_status
            
            return product_data
            
        except Exception as e:
            logger.error(f"Error extracting product data: {e}")
            return None
    
    def _extract_product_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product name from various possible selectors for Swiggy Instamart"""
        # Try to get from title tag first
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            if title_text and title_text != "Swiggy":
                return title_text
        
        # Try common selectors
        selectors = [
            'h1', 'h2', 'h3',
            '[class*="title"]', '[class*="name"]', '[class*="Title"]', '[class*="Name"]',
            '[class*="item"]', '[class*="product"]', '[class*="Item"]', '[class*="Product"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                text = element.get_text(strip=True)
                if text and len(text) > 3:  # Only meaningful text
                    return text
        
        # If we can't find a proper product name, try to extract from URL
        # This is a fallback for error pages
        return "Product (Page Error)"
    
    def _extract_prices(self, soup: BeautifulSoup) -> tuple:
        """Extract current and old prices for Swiggy Instamart"""
        current_price = None
        old_price = None
        
        # Try multiple selectors for current price
        current_price_selectors = [
            '[data-testid="price"]',
            '.price',
            '.current-price',
            '[class*="price"]',
            '.selling-price',
            # Swiggy specific selectors
            '.RestaurantMenuV2__ItemPrice',
            '[class*="ItemPrice"]',
            '[class*="Price"]',
            '.item-price',
            '.product-price',
            '[class*="CurrentPrice"]',
            '[class*="SellingPrice"]'
        ]
        
        for selector in current_price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                price_value = self._extract_price_value(price_text)
                if price_value:
                    current_price = price_value
                    break
        
        # Try to find old price (discounted price)
        old_price_selectors = [
            '.old-price',
            '.mrp',
            '.original-price',
            '[class*="old"]',
            '[class*="mrp"]',
            # Swiggy specific selectors
            '.RestaurantMenuV2__ItemPrice--old',
            '[class*="OldPrice"]',
            '[class*="OriginalPrice"]',
            '[class*="MRP"]',
            '.item-price-old',
            '.product-price-old'
        ]
        
        for selector in old_price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                price_value = self._extract_price_value(price_text)
                if price_value:
                    old_price = price_value
                    break
        
        return current_price, old_price
    
    def _extract_price_value(self, price_text: str) -> Optional[float]:
        """Extract numeric price value from text"""
        try:
            # Remove currency symbols and extract numbers
            import re
            # Find all numbers in the text
            numbers = re.findall(r'[\d,]+\.?\d*', price_text)
            if numbers:
                # Take the first number and convert to float
                price_str = numbers[0].replace(',', '')
                return float(price_str)
        except (ValueError, IndexError):
            pass
        return None
    
    def _extract_availability(self, soup: BeautifulSoup) -> tuple:
        """Extract availability status and stock information for Swiggy Instamart"""
        availability = "Unknown"
        stock_status = "Unknown"
        
        # Get all text content for analysis
        all_text = soup.get_text().lower()
        
        # Check for JavaScript error states first - but only if it's a product-specific error
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'ssrErrorState' in script.string:
                if '"isError":true' in script.string:
                    # Check if this is a general page error (itemData is null) vs product-specific error
                    if 'itemData' in script.string and 'null' in script.string:
                        # This is a general page error, not product-specific
                        availability = "Page Error"
                        stock_status = "Page Error"
                        return availability, stock_status
                    else:
                        # This might be a product-specific error
                        availability = "Out of Stock"
                        stock_status = "Out of Stock"
                        return availability, stock_status
        
        # Check for out of stock indicators
        out_of_stock_indicators = [
            'out of stock', 'not available', 'unavailable', 'sold out',
            'currently unavailable', 'not in stock', 'try again', 'error'
        ]
        
        # Check for available indicators
        available_indicators = [
            'add to cart', 'buy now', 'order now', 'available',
            'in stock', 'add', 'buy', 'order'
        ]
        
        # Check for out of stock
        if any(indicator in all_text for indicator in out_of_stock_indicators):
            availability = "Out of Stock"
            stock_status = "Unavailable"
        elif any(indicator in all_text for indicator in available_indicators):
            availability = "Available"
            stock_status = "In Stock"
        else:
            availability = "Unknown"
            stock_status = "Unknown"
        
        return availability, stock_status


def load_urls_from_file(file_path: str) -> list:
    """Load URLs from a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        logger.info(f"Loaded {len(urls)} URLs from {file_path}")
        return urls
    except FileNotFoundError:
        logger.error(f"URLs file not found: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Error loading URLs from file: {e}")
        return []


def validate_urls(urls: list) -> list:
    """Validate and filter URLs"""
    valid_urls = []
    fetcher = HTMLFetcher()
    
    for url in urls:
        if fetcher.is_valid_url(url):
            valid_urls.append(url)
        else:
            logger.warning(f"Invalid URL skipped: {url}")
    
    logger.info(f"Validated {len(valid_urls)} out of {len(urls)} URLs")
    return valid_urls


# Playwright stealth functions for Blinkit scraping
def fetch_html(url):
    """Fetches HTML content using a stealth-enabled browser for Blinkit scraping."""
    print(f"🚀 Launching STEALTH browser to fetch: {url}")
    html_content = None
    
    try:
        from playwright.sync_api import sync_playwright
        from playwright_stealth import stealth_sync
        
        with sync_playwright() as p:
            # --- IMPORTANT ---
            # For the first test run, we use headless=False to see the browser.
            # If it works, you can change it back to headless=True for automation.
            browser = p.chromium.launch(headless=False) 
            page = browser.new_page()
            
            # --- APPLYING THE CLOAKING DEVICE ---
            stealth_sync(page)
            
            # Go directly to the final URL
            page.goto(url, timeout=90000) # Increased timeout to 90 seconds

            # Wait for the product list to load
            print("⏳ Waiting for product list to load...")
            page.wait_for_selector("div.plp-product", timeout=60000) # Increased timeout
            
            print("✅ Page loaded successfully. Grabbing HTML...")
            html_content = page.content()
            
            # We'll leave the browser open for a few seconds to observe
            print("... Closing browser in 5 seconds.")
            page.wait_for_timeout(5000) 
            browser.close()
            
    except ImportError:
        print("❌ Playwright not available. Install with: pip install playwright playwright-stealth")
        return None
    except Exception as e:
        print(f"❌ Playwright Stealth Error: {e}")
        # Save a screenshot for debugging if anything goes wrong
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=60000)
                page.screenshot(path='error.png')
                print("📸 Screenshot 'error.png' saved for debugging.")
                browser.close()
        except Exception as ss_e:
            print(f"Could not take screenshot: {ss_e}")

    return html_content


if __name__ == "__main__":
    # Test the parser with a sample URL
    parser = SwiggyInstamartParser()
    test_url = "https://swiggy.com/sample-product"
    result = parser.parse_product_page(test_url)
    print(f"Test result: {result}")
