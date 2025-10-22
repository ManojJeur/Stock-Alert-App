# Scraper/scraper.py
from blinkit_scraper import scrape_blinkit_products, save_to_json
from utils import fetch_html
import schedule
import time

def job():
    """The job function that will be scheduled."""
    print("🚀 Starting scheduled scraping job...")
    
    city_slug = "mumbai"
    area_slug = "bandra-west" 
    search_query = "milk"
    
    # This is the correct direct URL format
    direct_url = f"https://blinkit.com/cn/{city_slug}/{area_slug}/pr/{search_query}"
    
    # STEP 1: Fetch the HTML content from the direct URL
    html_content = fetch_html(direct_url)
    
    # STEP 2: Pass the HTML content (not the URL) to the parsing function
    products = scrape_blinkit_products(html_content)
    
    if not products:
        print("❌ No products were parsed from the page.")
    else:
        save_to_json(products)
        
    print("\n✅ Scraping job complete. Waiting for the next run...")

def main():
    print("🕒 Scheduler started. Running the first job now...")
    job() 
    schedule.every(10).minutes.do(job)
    print("--> The next job will run in 10 minutes.")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()