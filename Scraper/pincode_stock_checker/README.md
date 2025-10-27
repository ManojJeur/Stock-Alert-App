# Pincode-wise Stock Checker

A comprehensive system for monitoring product availability across different pincodes and e-commerce platforms (Blinkit, Swiggy Instamart, Zepto) with WhatsApp alerts.

## Features

- **Multi-Platform Support**: Works with Blinkit, Swiggy Instamart, and Zepto
- **Pincode-wise Monitoring**: Check stock status for specific pincodes
- **WhatsApp Alerts**: Real-time notifications via Twilio WhatsApp API
- **Status Tracking**: Compare current vs previous stock status
- **Configurable**: Easy configuration via JSON files
- **Error Handling**: Robust error handling with retries
- **Logging**: Comprehensive logging system

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Copy `config.env` and update with your Twilio credentials
   - Update `config.json` with your products and pincodes

3. **Set up Twilio WhatsApp** (Optional):
   - Get Twilio account SID and auth token
   - Configure WhatsApp sandbox or production number
   - Update `config.env` with your credentials

## Configuration

### Environment Variables (`config.env`)

```env
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
RECIPIENT_PHONE_NUMBER=whatsapp:+1234567890

# Checker Configuration
CHECK_INTERVAL_MINUTES=10
MAX_RETRIES=3
RETRY_DELAY_SECONDS=5
```

### Product Configuration (`config.json`)

```json
{
    "pincodes": ["400001", "400002", "400003"],
    "products": {
        "Amul Butter 500g": {
            "url": "https://blinkit.com/products/amul-butter-500g",
            "platform": "blinkit"
        },
        "Coca Cola 600ml": {
            "url": "https://www.swiggy.com/instamart/item/0IFZHN76PS",
            "platform": "swiggy"
        }
    },
    "alert_settings": {
        "send_alerts": true,
        "alert_on_status_change": true,
        "alert_on_low_stock": true,
        "alert_on_oos": true,
        "alert_on_back_in_stock": true
    }
}
```

## Usage

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

## Alert Types

The system sends different types of alerts:

- **🚨 Out of Stock**: Product becomes unavailable
- **⚠️ Low Stock**: Product has limited availability
- **✅ Back in Stock**: Product becomes available again
- **📊 Status Change**: Any status change
- **❌ Error**: System errors or failures

## File Structure

```
pincode_stock_checker/
├── checker.py              # Main checker logic
├── alert.py                # WhatsApp alert system
├── platform_adapters.py   # Platform-specific adapters
├── config.json            # Product and pincode configuration
├── config.env             # Environment variables
├── requirements.txt        # Python dependencies
├── test_checker.py        # Test script
├── data/
│   └── last_status.json   # Previous status storage
└── README.md              # This file
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

## Testing

Run the test suite:
```bash
python test_checker.py
```

This will:
- Test alert system
- Test platform adapters
- Test main checker functionality

## Monitoring

The system creates detailed logs in `pincode_checker.log`:
- Stock check results
- Alert notifications
- Error messages
- Performance metrics

## Advanced Features

### Custom Platform Adapters
You can add support for new platforms by extending `BasePlatformAdapter`:

```python
class NewPlatformAdapter(BasePlatformAdapter):
    def get_stock_status(self, product_url: str, pincode: str):
        # Implement platform-specific logic
        pass
```

### Custom Alert Handlers
Extend the alert system for different notification methods:

```python
def custom_alert_handler(message: str, product_name: str, pincode: str):
    # Send email, SMS, or other notifications
    pass
```

## Troubleshooting

### Common Issues

1. **Twilio Configuration**:
   - Ensure correct account SID and auth token
   - Verify WhatsApp number format
   - Check sandbox vs production setup

2. **Platform Detection**:
   - Verify URL formats match supported platforms
   - Check for URL changes or redirects

3. **Stock Detection**:
   - Some platforms may have anti-bot measures
   - Adjust headers and request patterns
   - Implement delays between requests

### Debug Mode

Enable debug logging:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is open source and available under the MIT License.
