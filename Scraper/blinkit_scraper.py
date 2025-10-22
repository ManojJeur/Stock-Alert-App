# Scraper/blinkit_scraper.py
from bs4 import BeautifulSoup
from datetime import datetime
import json

def scrape_blinkit_products(html_content):
    """
    Scrape product name, price, and availability from the provided HTML content.
    """
    if not html_content:
        print("❌ HTML content is empty. Cannot parse products.")
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    products = []

    # The main container for each product is 'div.plp-product'
    product_cards = soup.find_all("div", class_="plp-product")

    for card in product_cards:
        # The product name is inside a div with itemprop="name"
        name_tag = card.find("div", itemprop="name")
        name = name_tag.text.strip() if name_tag else "Unnamed Product"

        # The price is inside a div with itemprop="price"
        price_tag = card.find("div", itemprop="price")
        price = f"₹{price_tag.text.strip()}" if price_tag else "N/A"

        # The stock status is determined by the text on the "Add" button
        button = card.find("button", class_="add-button")
        if button and "out of stock" in button.text.lower():
            stock = "Out of Stock"
        else:
            stock = "In Stock"

        products.append({
            "name": name,
            "price": price,
            "stock": stock
        })

    print(f"✅ Scraped {len(products)} products from the page.")
    return products

def save_to_json(data, filename="Scraper/sample_data.json"):
    """Save scraped data to a local JSON file with a timestamp."""
    output = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "products": data
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    print(f"💾 Data saved to {filename}")