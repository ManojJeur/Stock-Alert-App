"""
Database configuration and constants for Blinkit Product Scraper
"""

# Firebase Configuration
FIREBASE_CONFIG = {
    "apiKey": "your-api-key",
    "authDomain": "your-project.firebaseapp.com",
    "projectId": "your-project-id",
    "storageBucket": "your-project.appspot.com",
    "messagingSenderId": "123456789",
    "appId": "your-app-id"
}

# Firebase Collection Name
COLLECTION_NAME = "product_data"

# Scraping Configuration
SCRAPING_CONFIG = {
    "request_timeout": 30,
    "max_retries": 3,
    "retry_delay": 2,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Headers for requests to avoid blocking
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"'
}

# Table schema
PRODUCT_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS product_data (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(500) NOT NULL,
    current_price DECIMAL(10,2),
    old_price DECIMAL(10,2),
    availability VARCHAR(50),
    stock_status VARCHAR(100),
    product_url VARCHAR(1000),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_url)
);
"""

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
