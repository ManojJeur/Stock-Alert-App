# Blinkit Product Scraper

A production-ready web scraper for monitoring Blinkit product availability, prices, and stock status. This scraper is designed for the Stock Alert Dashboard system to provide real-time data for quick commerce brands.

## 🚀 Features

- **Automated Scraping**: Runs every 30 minutes automatically
- **PostgreSQL Integration**: Stores data in a structured database
- **Error Handling**: Robust retry logic and error recovery
- **Stock Monitoring**: Tracks availability and stock levels
- **Price Tracking**: Monitors current and discounted prices
- **Logging**: Comprehensive logging for monitoring and debugging
- **Modular Design**: Clean, maintainable code structure

## 📁 Project Structure

```
Scraper/
├── scraper.py          # Main scraper script
├── db.py               # Database operations
├── utils.py            # Utility functions
├── config.py           # Configuration settings
├── urls.txt            # Product URLs to monitor
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Internet connection

### Setup

1. **Clone the repository** (if not already done):
   ```bash
   cd D:\Projects\StockAlertDashboard\Scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database**:
   - Update `config.py` with your PostgreSQL credentials:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "database": "stock_alerts",
       "user": "postgres",
       "password": "yourpassword",
       "port": 5432
   }
   ```

4. **Create database** (if not exists):
   ```sql
   CREATE DATABASE stock_alerts;
   ```

5. **Add product URLs**:
   - Edit `urls.txt` and add Blinkit product URLs you want to monitor
   - One URL per line, comments start with #

## 🚀 Usage

### Command Line Interface

```bash
# Run single scraping session
python scraper.py scrape

# Start scheduled scraping (every 30 minutes)
python scraper.py schedule

# Show database statistics
python scraper.py stats

# Test database connection
python scraper.py test
```

### Interactive Mode

```bash
# Run without arguments for interactive menu
python scraper.py
```

### Programmatic Usage

```python
from scraper import BlinkitScraper

# Initialize scraper
scraper = BlinkitScraper()

# Run single scraping session
stats = scraper.scrape_all_products()

# Get database statistics
db_stats = scraper.get_database_stats()
```

## 📊 Database Schema

The scraper creates a `product_data` table with the following structure:

```sql
CREATE TABLE product_data (
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
```

## 🔧 Configuration

### Database Settings
Edit `config.py` to configure:
- Database connection details
- Request timeout and retry settings
- User agent for requests
- Logging configuration

### Scraping Settings
- **Request Timeout**: 30 seconds
- **Max Retries**: 3 attempts
- **Retry Delay**: 2 seconds (exponential backoff)
- **Request Delay**: 2 seconds between requests

## 📝 Logging

The scraper provides comprehensive logging:
- **Console Output**: Real-time status updates
- **Log File**: `scraper.log` for persistent logging
- **Log Levels**: INFO, WARNING, ERROR

## 🚨 Error Handling

The scraper handles various error scenarios:
- **Network Issues**: Automatic retry with exponential backoff
- **Invalid URLs**: Validation and filtering
- **Database Errors**: Connection retry and rollback
- **Parsing Errors**: Graceful failure with logging

## 📈 Monitoring

### Database Statistics
```python
stats = scraper.get_database_stats()
# Returns:
# {
#     'total_products': 150,
#     'available': 120,
#     'out_of_stock': 30,
#     'last_updated': '2025-01-21 10:35:00'
# }
```

### Scraping Statistics
```python
stats = scraper.scrape_all_products()
# Returns:
# {
#     'total_processed': 50,
#     'successful': 45,
#     'failed': 5,
#     'updated': 40,
#     'new': 5
# }
```

## 🔄 Scheduling

The scraper can run in two modes:

1. **Manual**: Run single scraping sessions on demand
2. **Scheduled**: Automatic scraping every 30 minutes

### Starting Scheduled Mode
```bash
python scraper.py schedule
```

### Stopping Scheduled Mode
Press `Ctrl+C` to stop the scheduler.

## 🛡️ Best Practices

1. **Respectful Scraping**: 2-second delay between requests
2. **Error Recovery**: Automatic retry with exponential backoff
3. **Data Validation**: URL validation and data sanitization
4. **Logging**: Comprehensive logging for monitoring
5. **Database Integrity**: UPSERT operations to prevent duplicates

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify credentials in `config.py`
   - Ensure database exists

2. **No Products Scraped**
   - Check URLs in `urls.txt` are valid
   - Verify internet connection
   - Check if Blinkit is blocking requests

3. **Parsing Errors**
   - Blinkit may have changed their HTML structure
   - Update selectors in `utils.py` if needed

### Debug Mode
Enable debug logging by modifying `config.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For issues or questions:
1. Check the logs in `scraper.log`
2. Verify database connection
3. Test with a single URL first
4. Check Blinkit's robots.txt for any restrictions

## 🔄 Updates

To update the scraper:
1. Backup your `urls.txt` file
2. Update the code
3. Test with a few URLs first
4. Monitor logs for any issues

## 📋 Example Output

```
2025-01-21 10:35:00 - INFO - Starting product scraping session
2025-01-21 10:35:01 - INFO - Loaded 5 valid URLs for scraping
2025-01-21 10:35:02 - INFO - Processing product 1/5: https://blinkit.com/products/amul-butter-500g
2025-01-21 10:35:05 - INFO - Successfully stored product: Amul Butter 500g
2025-01-21 10:35:07 - INFO - Processing product 2/5: https://blinkit.com/products/maggi-noodles
2025-01-21 10:35:10 - INFO - Successfully stored product: Maggi Noodles 2-Minute Masala
...
2025-01-21 10:35:25 - INFO - ==================================================
2025-01-21 10:35:25 - INFO - SCRAPING SESSION COMPLETED
2025-01-21 10:35:25 - INFO - ==================================================
2025-01-21 10:35:25 - INFO - Total products processed: 5
2025-01-21 10:35:25 - INFO - Successfully scraped: 5
2025-01-21 10:35:25 - INFO - Failed to scrape: 0
2025-01-21 10:35:25 - INFO - Execution time: 25.30 seconds
2025-01-21 10:35:25 - INFO - ==================================================
```

## 🎯 Integration with Stock Alert Dashboard

This scraper is designed to work with the Stock Alert Dashboard system:

1. **Data Source**: Provides real-time product data
2. **Alert Triggers**: Stock status changes trigger alerts
3. **Price Monitoring**: Price changes can trigger notifications
4. **Availability Tracking**: Out-of-stock products trigger alerts

The scraper feeds data into the PostgreSQL database, which is then consumed by the dashboard and alert system.
