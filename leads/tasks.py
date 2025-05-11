from celery import shared_task
import requests
import json
from django.conf import settings
import logging
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(email, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    logger.info(f"Email task executed for {email}")
    print(f"Email sent to {email}")

@shared_task
def send_whatsapp_task(phone_number, name):
    _send_whatsapp(phone_number, name)

@shared_task
def send_followup_whatsapp_task(phone_number, name, step):
    message_suffix = {
        2: "Here’s some more info you might find useful.",
        3: "Final follow-up! Feel free to reply if you have any questions."
    }
    followup_text = f"{name}, {message_suffix.get(step, '')}"
    _send_whatsapp(phone_number, followup_text)

def _send_whatsapp(phone_number, name_or_text):
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
                            "text": name_or_text
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    logger.info(f"WhatsApp Response ({response.status_code}): {response.text}")
    print(f"WhatsApp sent to {phone_number}: {response.text}")
