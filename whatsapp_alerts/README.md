# WhatsApp Stock Alert System (Twilio Sandbox)

This module sends WhatsApp alerts using Twilio's WhatsApp Sandbox. It is designed to later switch to the Official WhatsApp Business API with minimal changes.

## Requirements

- Python 3.10+
- Install dependencies:

```bash
pip install twilio python-dotenv
```

## Environment Variables

Create a `.env` file in this folder using the following template:

```
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=whatsapp:+14155238886
RECEIVER_NUMBER=whatsapp:+91XXXXXXXXXX
```

Notes:
- `TWILIO_FROM_NUMBER` uses the Sandbox number during testing: `whatsapp:+14155238886`.
- `RECEIVER_NUMBER` must be the same number you verified in Twilio and joined to the sandbox.

## Twilio Sandbox Setup

1. Create a free account: https://www.twilio.com/try-twilio
2. Verify your phone number
3. Navigate: Messaging → Try it out → WhatsApp Sandbox
4. Note the sandbox number `+14155238886` and your unique join code (e.g., `join solar-wave`)
5. Send the join code via WhatsApp to the sandbox number

## Run

```bash
python whatsapp_alerts/alert.py
```

Expected output:

```
✅ Alert sent successfully! SID: SMxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

And on WhatsApp:

```
🚨 ALERT: Product 'Amul Butter' is out of stock in Pincode 400001!
```

## Integrate with a Scraper

```python
from whatsapp_alerts.alert import send_whatsapp_alert

if stock_status == "Low":
    send_whatsapp_alert("⚠️ Low stock alert for Dettol in 400001!")
elif stock_status == "Out of Stock":
    send_whatsapp_alert("🚨 OOS alert for Dettol in 400001! Restock ASAP.")
```

## Move to Production (Official API)

Update your `.env` with your business number and production credentials:

```
TWILIO_FROM_NUMBER=whatsapp:+91XXXXXXXXXX
```

No code changes required.


