# 🚀 Quick Start Guide - Blinkit Product Scraper

## ⚡ Get Started in 5 Minutes

### 1. Install Dependencies
```bash
cd Scraper
pip install -r requirements.txt
```

### 2. Configure Database
Edit `config.py` with your PostgreSQL details:
```python
DB_CONFIG = {
    "host": "localhost",
    "database": "stock_alerts", 
    "user": "postgres",
    "password": "yourpassword",
    "port": 5432
}
```

### 3. Create Database
```sql
CREATE DATABASE stock_alerts;
```

### 4. Add Product URLs
Edit `urls.txt` and add Blinkit product URLs:
```
https://blinkit.com/products/amul-butter-500g
https://blinkit.com/products/maggi-noodles-2-minute-masala
```

### 5. Test Everything
```bash
python test_scraper.py
```

### 6. Run the Scraper
```bash
# Single scraping session
python scraper.py scrape

# Automatic scraping every 30 minutes
python scraper.py schedule

# Show database statistics
python scraper.py stats
```

## 📁 File Structure
```
Scraper/
├── scraper.py          # 🎯 Main scraper script
├── db.py               # 🗄️ Database operations
├── utils.py            # 🔧 Utility functions
├── config.py           # ⚙️ Configuration
├── urls.txt            # 📝 Product URLs
├── requirements.txt    # 📦 Dependencies
├── setup.py            # 🛠️ Setup script
├── test_scraper.py     # 🧪 Test script
├── example_usage.py    # 📚 Usage examples
└── README.md           # 📖 Full documentation
```

## 🎯 Key Features
- ✅ **Automated Scraping**: Every 30 minutes
- ✅ **PostgreSQL Integration**: Structured data storage
- ✅ **Error Handling**: Robust retry logic
- ✅ **Stock Monitoring**: Availability tracking
- ✅ **Price Tracking**: Current and discounted prices
- ✅ **Logging**: Comprehensive monitoring
- ✅ **Modular Design**: Clean, maintainable code

## 🔧 Commands
```bash
python scraper.py scrape      # Run once
python scraper.py schedule     # Run every 30 min
python scraper.py stats       # Show statistics
python scraper.py test        # Test connection
python setup.py              # Setup wizard
python test_scraper.py       # Run tests
python example_usage.py     # See examples
```

## 📊 Database Schema
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

## 🚨 Troubleshooting
- **Database Error**: Check PostgreSQL is running
- **No Data**: Verify URLs in `urls.txt`
- **Parsing Error**: Blinkit may have changed HTML structure

## 📞 Need Help?
1. Check `scraper.log` for detailed logs
2. Run `python test_scraper.py` to diagnose issues
3. See `README.md` for full documentation

---
**Ready to monitor Blinkit products? Start with `python scraper.py scrape`!** 🎉
