"""
Setup script for Blinkit Product Scraper
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        from db import test_connection
        if test_connection():
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed!")
            print("Please check your database configuration in config.py")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def create_sample_urls():
    """Create sample URLs file if it doesn't exist"""
    urls_file = Path("urls.txt")
    if not urls_file.exists():
        print("Creating sample URLs file...")
        with open(urls_file, 'w') as f:
            f.write("""# Blinkit Product URLs for Stock Alert Dashboard
# Add your Blinkit product URLs here, one per line
# Lines starting with # are comments and will be ignored

# Example URLs (replace with actual Blinkit product URLs):
# https://blinkit.com/products/amul-butter-500g
# https://blinkit.com/products/maggi-noodles-2-minute-masala
# https://blinkit.com/products/coca-cola-600ml

# Instructions:
# 1. Visit Blinkit.com and find products you want to monitor
# 2. Copy the product URLs and paste them below
# 3. Remove the # symbol from the beginning of each URL
# 4. Save this file
# 5. Run the scraper to start monitoring these products
""")
        print("✅ Sample URLs file created!")
    else:
        print("✅ URLs file already exists!")

def main():
    """Main setup function"""
    print("🚀 Setting up Blinkit Product Scraper...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return False
    
    # Create sample URLs file
    create_sample_urls()
    
    # Test database connection
    db_ok = test_database_connection()
    
    print("=" * 50)
    if db_ok:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Add product URLs to urls.txt")
        print("2. Run: python scraper.py test")
        print("3. Run: python scraper.py scrape")
        print("4. Run: python scraper.py schedule (for automatic scraping)")
    else:
        print("⚠️  Setup completed with warnings!")
        print("\nPlease:")
        print("1. Check your database configuration in config.py")
        print("2. Ensure PostgreSQL is running")
        print("3. Create the 'stock_alerts' database")
        print("4. Run: python scraper.py test")
    
    return True

if __name__ == "__main__":
    main()
