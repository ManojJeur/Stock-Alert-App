# Pincode Stock Checker - Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `config.env` with your Twilio credentials:
```env
TWILIO_ACCOUNT_SID=your_actual_account_sid
TWILIO_AUTH_TOKEN=your_actual_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
RECIPIENT_PHONE_NUMBER=whatsapp:+1234567890
```

### 3. Configure Products and Pincodes
Edit `config.json` with your products:
```json
{
    "pincodes": ["400001", "400002", "400003"],
    "products": {
        "Your Product Name": {
            "url": "https://platform.com/product-url",
            "platform": "blinkit|swiggy|zepto"
        }
    }
}
```

### 4. Test the System
```bash
python demo.py
```

### 5. Run the Checker
```bash
# Single check
python checker.py --mode once

# Continuous monitoring
python checker.py --mode continuous
```

## Features

✅ **Multi-Platform Support**: Blinkit, Swiggy Instamart, Zepto
✅ **Pincode-wise Monitoring**: Check stock for specific locations
✅ **WhatsApp Alerts**: Real-time notifications via Twilio
✅ **Status Tracking**: Compare current vs previous status
✅ **Error Handling**: Robust retry logic and error recovery
✅ **Configurable**: Easy JSON configuration
✅ **Logging**: Comprehensive logging system

## Alert Types

- 🚨 **Out of Stock**: Product becomes unavailable
- ⚠️ **Low Stock**: Product has limited availability  
- ✅ **Back in Stock**: Product becomes available again
- 📊 **Status Change**: Any status change
- ❌ **Error**: System errors or failures

## File Structure

```
pincode_stock_checker/
├── checker.py              # Main checker logic
├── alert.py                # WhatsApp alert system
├── platform_adapters.py    # Platform-specific adapters
├── config.json            # Product configuration
├── config.env             # Environment variables
├── demo.py                # Demo script
├── test_checker.py        # Test script
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── SETUP_GUIDE.md         # This file
└── data/
    └── last_status.json   # Status storage
```

## Platform Support

### Blinkit
- URL format: `https://blinkit.com/products/product-name`
- Detects: Available, Low Stock, Out of Stock
- Price extraction supported

### Swiggy Instamart  
- URL format: `https://www.swiggy.com/instamart/item/item-id`
- Detects: Available, Low Stock, Out of Stock, Page Errors
- JavaScript error state detection

### Zepto
- URL format: `https://zepto.com/products/product-name`
- Detects: Available, Low Stock, Out of Stock
- Price extraction supported

## Usage Examples

### Single Check
```bash
python checker.py --mode once
```

### Continuous Monitoring
```bash
python checker.py --mode continuous
```

### Custom Configuration
```bash
python checker.py --config my_config.json --mode continuous
```

## Troubleshooting

### Twilio Authentication Error
- Ensure correct account SID and auth token
- Verify WhatsApp number format
- Check sandbox vs production setup

### Platform Detection Issues
- Verify URL formats match supported platforms
- Check for URL changes or redirects

### Stock Detection Problems
- Some platforms have anti-bot measures
- Adjust headers and request patterns
- Implement delays between requests

## Advanced Configuration

### Custom Alert Settings
```json
{
    "alert_settings": {
        "send_alerts": true,
        "alert_on_status_change": true,
        "alert_on_low_stock": true,
        "alert_on_oos": true,
        "alert_on_back_in_stock": true,
        "send_daily_summary": false
    }
}
```

### Environment Variables
```env
CHECK_INTERVAL_MINUTES=10
MAX_RETRIES=3
RETRY_DELAY_SECONDS=5
```

## Monitoring

The system creates detailed logs in `pincode_checker.log`:
- Stock check results
- Alert notifications
- Error messages
- Performance metrics

## Support

For issues or questions:
1. Check the logs in `pincode_checker.log`
2. Run `python test_checker.py` to verify setup
3. Check Twilio configuration in `config.env`
4. Verify product URLs in `config.json`
