"""
Debug Swiggy Instamart page to understand the actual structure
"""

import requests
from bs4 import BeautifulSoup
from config import REQUEST_HEADERS
import json

def debug_swiggy_page(url):
    """Debug the Swiggy page to understand the structure"""
    print(f"Debugging Swiggy page: {url}")
    print("=" * 60)
    
    try:
        # Fetch the page
        session = requests.Session()
        session.headers.update(REQUEST_HEADERS)
        response = session.get(url, timeout=30)
        
        if response.status_code == 200:
            print("Successfully fetched page")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for JavaScript data
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'ssrErrorState' in script.string:
                    print("\nFound ssrErrorState in JavaScript:")
                    # Extract the JSON data
                    script_content = script.string
                    if 'window.___INITIAL_STATE___' in script_content:
                        # Find the JSON part
                        start = script_content.find('window.___INITIAL_STATE___ = ')
                        if start != -1:
                            start = script_content.find('{', start)
                            # Find the end of the JSON object
                            brace_count = 0
                            end = start
                            for i, char in enumerate(script_content[start:], start):
                                if char == '{':
                                    brace_count += 1
                                elif char == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        end = i + 1
                                        break
                            
                            json_str = script_content[start:end]
                            try:
                                data = json.loads(json_str)
                                print(f"ssrErrorState: {data.get('instamart', {}).get('ssrErrorState', {})}")
                                
                                # Check if there's actual product data
                                product_data = data.get('instamart', {}).get('productV2', {})
                                print(f"Product data: {product_data}")
                                
                                # Check for item data
                                item_data = product_data.get('itemData')
                                if item_data:
                                    print(f"Item found: {item_data.get('name', 'Unknown')}")
                                    print(f"Item availability: {item_data.get('inStock', 'Unknown')}")
                                    print(f"Item price: {item_data.get('price', 'Unknown')}")
                                else:
                                    print("No item data found")
                                    
                            except json.JSONDecodeError as e:
                                print(f"Error parsing JSON: {e}")
            
            # Look for any buttons or elements that might indicate availability
            print("\nLooking for availability indicators...")
            
            # Check for "Add to Cart" buttons
            add_buttons = soup.find_all(['button', 'div'], string=lambda text: text and any(word in text.lower() for word in ['add', 'cart', 'buy']))
            print(f"Add to cart buttons found: {len(add_buttons)}")
            for i, button in enumerate(add_buttons[:3]):
                print(f"  {i+1}. {button.get_text(strip=True)}")
            
            # Check for any text indicating availability
            availability_text = soup.find_all(string=lambda text: text and any(word in text.lower() for word in ['available', 'in stock', 'add to cart', 'buy now']))
            print(f"Availability text found: {len(availability_text)}")
            for i, text in enumerate(availability_text[:5]):
                print(f"  {i+1}. {text.strip()}")
            
            # Check for any error messages
            error_text = soup.find_all(string=lambda text: text and any(word in text.lower() for word in ['error', 'unavailable', 'out of stock', 'not available']))
            print(f"Error text found: {len(error_text)}")
            for i, text in enumerate(error_text[:5]):
                print(f"  {i+1}. {text.strip()}")
            
            # Look for product name in the page
            print("\nLooking for product name...")
            name_selectors = [
                'h1', 'h2', 'h3', '[class*="name"]', '[class*="title"]', 
                '[class*="product"]', '[class*="item"]'
            ]
            
            for selector in name_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 3 and len(text) < 100:  # Reasonable product name length
                        print(f"Potential product name: {text}")
                        break
                if elements:
                    break
            
            print("\n" + "=" * 60)
            print("Debug completed!")
            
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error debugging page: {e}")

if __name__ == "__main__":
    # Test with the Swiggy URL
    url = "https://www.swiggy.com/instamart/item/0IFZHN76PS"
    debug_swiggy_page(url)
