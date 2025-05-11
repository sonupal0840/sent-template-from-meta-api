import requests
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def send_email_to_lead_sync(email, subject, message):
    if not getattr(settings, 'EMAIL_HOST_USER', None):
        logger.error("EMAIL_HOST_USER not configured in settings.py")
        return
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        logger.info(f"Email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}")

def send_whatsapp_message_sync(phone, name):
    if not phone:
        logger.error("Phone number is missing.")
        return {"error": "Phone number is required."}
    if not phone.startswith("+"):
        phone = "+91" + phone  # Default to Indian format

    phone_number_id = getattr(settings, 'META_PHONE_NUMBER_ID', None)
    access_token = getattr(settings, 'META_ACCESS_TOKEN', None)

    if not phone_number_id or not access_token:
        logger.error("WhatsApp API credentials missing in settings.py")
        return {"error": "Missing WhatsApp API configuration."}

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # WhatsApp template message payload
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": "account_creation",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": name
                        }
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f"WhatsApp Response ({response.status_code}): {response.text}")
        print(f"WhatsApp sent to {phone}: {response.text}")
        if response.status_code == 200:
            logger.info(f"WhatsApp message sent successfully to {phone}")
        return response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}", "response": response.text}
    
    except requests.RequestException as e:
        logger.error(f"RequestException while sending WhatsApp message: {e}")
        return {"error": "RequestException", "details": str(e)}
