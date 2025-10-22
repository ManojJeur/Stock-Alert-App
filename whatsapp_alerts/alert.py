import os
from twilio.rest import Client
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Twilio setup
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")  # e.g. whatsapp:+14155238886 (Sandbox)
TO_NUMBER = os.getenv("RECEIVER_NUMBER")       # e.g. whatsapp:+91XXXXXXXXXX

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_whatsapp_alert(message_text: str) -> None:

    message = client.messages.create(
        from_=FROM_NUMBER,
        body=message_text,
        to=TO_NUMBER,
    )
    print(f"✅ Alert sent successfully! SID: {message.sid}")


if __name__ == "__main__":
    send_whatsapp_alert(
        "🚨 ALERT: Product 'Amul Butter' is out of stock in Pincode 400001!"
    )


