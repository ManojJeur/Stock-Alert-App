"""
Check stock status for all products in Firebase
"""

from db import get_db_connection

def check_stock_status():
    """Check and display stock status for all products"""
    print("Stock Status Check")
    print("=" * 50)
    
    try:
        with get_db_connection() as db:
            products = db.get_all_products()
            
            if not products:
                print("No products found in database")
                return
            
            print(f"Found {len(products)} products:")
            print()
            
            for i, product in enumerate(products, 1):
                print(f"{i}. Product: {product.get('product_name', 'Unknown')}")
                print(f"   URL: {product.get('product_url', 'Unknown')}")
                print(f"   Availability: {product.get('availability', 'Unknown')}")
                print(f"   Stock Status: {product.get('stock_status', 'Unknown')}")
                print(f"   Price: Rs {product.get('current_price', 'N/A')}")
                print(f"   Last Updated: {product.get('timestamp', 'Unknown')}")
                print("-" * 40)
            
            # Summary
            available_count = sum(1 for p in products if p.get('availability') == 'Available')
            out_of_stock_count = sum(1 for p in products if p.get('availability') == 'Out of Stock')
            
            print(f"\nSummary:")
            print(f"Total Products: {len(products)}")
            print(f"In Stock: {available_count}")
            print(f"Out of Stock: {out_of_stock_count}")
            
    except Exception as e:
        print(f"Error checking stock status: {e}")

if __name__ == "__main__":
    check_stock_status()
