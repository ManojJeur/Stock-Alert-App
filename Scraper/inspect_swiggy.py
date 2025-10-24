"""
Inspect Swiggy Instamart page structure to find stock indicators
"""

import requests
from bs4 import BeautifulSoup
from config import REQUEST_HEADERS

def inspect_swiggy_page(url):
    """Inspect the Swiggy page structure"""
    print(f"Inspecting Swiggy page: {url}")
    print("=" * 60)
    
    try:
        # Fetch the page
        session = requests.Session()
        session.headers.update(REQUEST_HEADERS)
        response = session.get(url, timeout=30)
        
        if response.status_code == 200:
            print("Successfully fetched page")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for common stock indicators
            print("\nLooking for stock indicators...")
            
            # Check for "Add to Cart" buttons
            add_to_cart_buttons = soup.find_all(['button', 'div'], string=lambda text: text and 'add' in text.lower() and 'cart' in text.lower())
            print(f"Add to Cart buttons found: {len(add_to_cart_buttons)}")
            for i, button in enumerate(add_to_cart_buttons[:3]):  # Show first 3
                print(f"   {i+1}. {button.get_text(strip=True)}")
            
            # Check for "Out of Stock" indicators
            out_of_stock_indicators = soup.find_all(string=lambda text: text and any(word in text.lower() for word in ['out of stock', 'unavailable', 'not available', 'sold out']))
            print(f"Out of Stock indicators found: {len(out_of_stock_indicators)}")
            for i, indicator in enumerate(out_of_stock_indicators[:3]):  # Show first 3
                print(f"   {i+1}. {indicator.strip()}")
            
            # Check for "Currently unavailable" text
            unavailable_text = soup.find_all(string=lambda text: text and 'currently unavailable' in text.lower())
            print(f"Currently unavailable text found: {len(unavailable_text)}")
            for i, text in enumerate(unavailable_text[:3]):
                print(f"   {i+1}. {text.strip()}")
            
            # Look for price elements
            price_elements = soup.find_all(['span', 'div'], class_=lambda x: x and 'price' in x.lower())
            print(f"Price elements found: {len(price_elements)}")
            for i, price in enumerate(price_elements[:3]):
                print(f"   {i+1}. {price.get_text(strip=True)}")
            
            # Look for product name
            name_elements = soup.find_all(['h1', 'h2', 'h3'], class_=lambda x: x and any(word in x.lower() for word in ['name', 'title', 'item']))
            print(f"Product name elements found: {len(name_elements)}")
            for i, name in enumerate(name_elements[:3]):
                print(f"   {i+1}. {name.get_text(strip=True)}")
            
            # Look for buttons with specific classes
            buttons = soup.find_all('button')
            print(f"Total buttons found: {len(buttons)}")
            
            # Check button text for stock indicators
            stock_buttons = []
            for button in buttons:
                text = button.get_text(strip=True).lower()
                if any(word in text for word in ['add', 'cart', 'buy', 'unavailable', 'out of stock']):
                    stock_buttons.append(button)
            
            print(f"Buttons with stock-related text: {len(stock_buttons)}")
            for i, button in enumerate(stock_buttons[:5]):  # Show first 5
                print(f"   {i+1}. Text: '{button.get_text(strip=True)}'")
                print(f"      Classes: {button.get('class', [])}")
            
            # Look for specific Swiggy classes
            swiggy_classes = soup.find_all(class_=lambda x: x and any(word in str(x).lower() for word in ['add', 'cart', 'button', 'unavailable', 'stock']))
            print(f"Elements with stock-related classes: {len(swiggy_classes)}")
            for i, element in enumerate(swiggy_classes[:5]):
                print(f"   {i+1}. Tag: {element.name}, Classes: {element.get('class', [])}")
                print(f"      Text: {element.get_text(strip=True)[:50]}...")
            
            # Check for data attributes
            data_attrs = soup.find_all(attrs={'data-testid': True})
            print(f"Elements with data-testid: {len(data_attrs)}")
            for i, element in enumerate(data_attrs[:10]):
                testid = element.get('data-testid')
                if any(word in testid.lower() for word in ['add', 'cart', 'button', 'stock', 'unavailable']):
                    print(f"   {i+1}. data-testid: '{testid}'")
                    print(f"      Text: {element.get_text(strip=True)[:30]}...")
            
            print("\n" + "=" * 60)
            print("Inspection completed!")
            
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error inspecting page: {e}")

if __name__ == "__main__":
    # Test with the Swiggy URL
    url = "https://www.swiggy.com/instamart/item/0IFZHN76PS"
    inspect_swiggy_page(url)