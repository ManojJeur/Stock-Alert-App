# Scraper/utils.py
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def fetch_html(url):
    """Fetches HTML content using a stealth-enabled browser."""
    print(f"🚀 Launching STEALTH browser to fetch: {url}")
    html_content = None
    
    try:
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
            
    except Exception as e:
        print(f"❌ Playwright Stealth Error: {e}")
        # Save a screenshot for debugging if anything goes wrong
        try:
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