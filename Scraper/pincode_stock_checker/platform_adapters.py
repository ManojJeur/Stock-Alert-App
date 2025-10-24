"""
Platform-specific adapters for different e-commerce platforms
Handles pincode-specific stock checking for Blinkit, Zepto, and Swiggy Instamart
"""

import requests
import logging
from bs4 import BeautifulSoup
from typing import Dict, Optional, Tuple
import time
import json

logger = logging.getLogger(__name__)

class BasePlatformAdapter:
    """Base class for platform adapters"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        self.session.headers.update(self.headers)
    
    def get_stock_status(self, product_url: str, pincode: str) -> Tuple[str, str, Optional[float]]:
        """
        Get stock status for a product in a specific pincode
        
        Returns:
            Tuple of (status, stock_level, price)
            status: "Available", "Low", "OOS", "Error"
            stock_level: "In Stock", "Limited", "Out of Stock", "Error"
            price: float or None
        """
        raise NotImplementedError("Subclasses must implement get_stock_status")
    
    def _fetch_page(self, url: str, pincode: str = None) -> Optional[BeautifulSoup]:
        """Fetch and parse page content"""
        try:
            # Add pincode to headers if supported
            headers = self.headers.copy()
            if pincode:
                headers['X-Pincode'] = pincode
                headers['Pincode'] = pincode
            
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing page {url}: {e}")
            return None

class BlinkitAdapter(BasePlatformAdapter):
    """Adapter for Blinkit platform"""
    
    def get_stock_status(self, product_url: str, pincode: str) -> Tuple[str, str, Optional[float]]:
        """Get Blinkit stock status for specific pincode"""
        soup = self._fetch_page(product_url, pincode)
        if not soup:
            return "Error", "Error", None
        
        try:
            # Extract product name
            product_name = self._extract_product_name(soup)
            
            # Extract stock status
            stock_status, stock_level = self._extract_stock_status(soup)
            
            # Extract price
            price = self._extract_price(soup)
            
            return stock_status, stock_level, price
            
        except Exception as e:
            logger.error(f"Error processing Blinkit product {product_url}: {e}")
            return "Error", "Error", None
    
    def _extract_product_name(self, soup: BeautifulSoup) -> str:
        """Extract product name from Blinkit page"""
        selectors = [
            'h1', '.product-title', '[class*="title"]', '[class*="name"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
        
        return "Unknown Product"
    
    def _extract_stock_status(self, soup: BeautifulSoup) -> Tuple[str, str]:
        """Extract stock status from Blinkit page"""
        # Check for out of stock indicators
        out_of_stock_text = [
            'out of stock', 'not available', 'unavailable', 'sold out',
            'currently unavailable', 'not in stock'
        ]
        
        page_text = soup.get_text().lower()
        
        for indicator in out_of_stock_text:
            if indicator in page_text:
                return "OOS", "Out of Stock"
        
        # Check for low stock indicators
        low_stock_text = [
            'only few left', 'limited stock', 'few left', 'hurry',
            'only 1 left', 'only 2 left', 'only 3 left'
        ]
        
        for indicator in low_stock_text:
            if indicator in page_text:
                return "Low", "Limited Stock"
        
        # Check for available indicators
        available_text = [
            'add to cart', 'buy now', 'order now', 'available',
            'in stock', 'add', 'buy'
        ]
        
        for indicator in available_text:
            if indicator in page_text:
                return "Available", "In Stock"
        
        return "Unknown", "Unknown"
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract price from Blinkit page"""
        price_selectors = [
            '.price', '.current-price', '.selling-price', '[class*="price"]'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # Extract numeric value
                import re
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                if price_match:
                    try:
                        return float(price_match.group())
                    except ValueError:
                        continue
        
        return None

class SwiggyInstamartAdapter(BasePlatformAdapter):
    """Adapter for Swiggy Instamart platform"""
    
    def get_stock_status(self, product_url: str, pincode: str) -> Tuple[str, str, Optional[float]]:
        """Get Swiggy Instamart stock status for specific pincode"""
        soup = self._fetch_page(product_url, pincode)
        if not soup:
            return "Error", "Error", None
        
        try:
            # Check for JavaScript error states
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'ssrErrorState' in script.string:
                    if '"isError":true' in script.string:
                        if 'itemData' in script.string and 'null' in script.string:
                            return "Error", "Page Error", None
                        else:
                            return "OOS", "Out of Stock", None
            
            # Extract stock status
            stock_status, stock_level = self._extract_stock_status(soup)
            
            # Extract price
            price = self._extract_price(soup)
            
            return stock_status, stock_level, price
            
        except Exception as e:
            logger.error(f"Error processing Swiggy product {product_url}: {e}")
            return "Error", "Error", None
    
    def _extract_stock_status(self, soup: BeautifulSoup) -> Tuple[str, str]:
        """Extract stock status from Swiggy page"""
        # Check for out of stock indicators
        out_of_stock_indicators = [
            'out of stock', 'not available', 'unavailable', 'sold out',
            'currently unavailable', 'not in stock'
        ]
        
        page_text = soup.get_text().lower()
        
        for indicator in out_of_stock_indicators:
            if indicator in page_text:
                return "OOS", "Out of Stock"
        
        # Check for low stock indicators
        low_stock_indicators = [
            'only few left', 'limited stock', 'few left', 'hurry',
            'only 1 left', 'only 2 left', 'only 3 left'
        ]
        
        for indicator in low_stock_indicators:
            if indicator in page_text:
                return "Low", "Limited Stock"
        
        # Check for available indicators
        available_indicators = [
            'add to cart', 'buy now', 'order now', 'available',
            'in stock', 'add', 'buy'
        ]
        
        for indicator in available_indicators:
            if indicator in page_text:
                return "Available", "In Stock"
        
        return "Unknown", "Unknown"
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract price from Swiggy page"""
        price_selectors = [
            '.price', '.current-price', '.selling-price', '[class*="price"]'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # Extract numeric value
                import re
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                if price_match:
                    try:
                        return float(price_match.group())
                    except ValueError:
                        continue
        
        return None

class ZeptoAdapter(BasePlatformAdapter):
    """Adapter for Zepto platform"""
    
    def get_stock_status(self, product_url: str, pincode: str) -> Tuple[str, str, Optional[float]]:
        """Get Zepto stock status for specific pincode"""
        soup = self._fetch_page(product_url, pincode)
        if not soup:
            return "Error", "Error", None
        
        try:
            # Extract stock status
            stock_status, stock_level = self._extract_stock_status(soup)
            
            # Extract price
            price = self._extract_price(soup)
            
            return stock_status, stock_level, price
            
        except Exception as e:
            logger.error(f"Error processing Zepto product {product_url}: {e}")
            return "Error", "Error", None
    
    def _extract_stock_status(self, soup: BeautifulSoup) -> Tuple[str, str]:
        """Extract stock status from Zepto page"""
        # Similar logic to other adapters
        page_text = soup.get_text().lower()
        
        # Check for out of stock
        if any(indicator in page_text for indicator in ['out of stock', 'not available', 'unavailable']):
            return "OOS", "Out of Stock"
        
        # Check for low stock
        if any(indicator in page_text for indicator in ['only few left', 'limited stock', 'few left']):
            return "Low", "Limited Stock"
        
        # Check for available
        if any(indicator in page_text for indicator in ['add to cart', 'buy now', 'available']):
            return "Available", "In Stock"
        
        return "Unknown", "Unknown"
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract price from Zepto page"""
        price_selectors = [
            '.price', '.current-price', '.selling-price', '[class*="price"]'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                import re
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                if price_match:
                    try:
                        return float(price_match.group())
                    except ValueError:
                        continue
        
        return None

# Platform registry
PLATFORM_ADAPTERS = {
    'blinkit': BlinkitAdapter,
    'swiggy': SwiggyInstamartAdapter,
    'zepto': ZeptoAdapter
}

def get_platform_adapter(platform: str) -> BasePlatformAdapter:
    """Get platform adapter by name"""
    adapter_class = PLATFORM_ADAPTERS.get(platform.lower())
    if not adapter_class:
        raise ValueError(f"Unsupported platform: {platform}")
    return adapter_class()

def detect_platform_from_url(url: str) -> str:
    """Detect platform from URL"""
    url_lower = url.lower()
    if 'blinkit.com' in url_lower:
        return 'blinkit'
    elif 'swiggy.com' in url_lower:
        return 'swiggy'
    elif 'zepto.com' in url_lower:
        return 'zepto'
    else:
        return 'unknown'
