import requests
import json
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_whatsapp(phone_number, name):
    body_text = name  # This will be inserted in the body placeholder
    _send_whatsapp(phone_number, body_text)

def send_followup_whatsapp(phone_number, name, step):
    message_suffix = {
        2: "Here’s some more info you might find useful.",
        3: "Final follow-up! Feel free to reply if you have any questions."
    }
    followup_text = f"{name}, {message_suffix.get(step, '')}"
    _send_whatsapp(phone_number, followup_text)

def _send_whatsapp(phone_number, body_text):
    url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "account_creation_confirmation_3",  # Make sure this is your correct template name
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": body_text
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    logger.info(f"WhatsApp Response ({response.status_code}): {response.text}")
    print(f"WhatsApp sent to {phone_number}: {response.text}")
