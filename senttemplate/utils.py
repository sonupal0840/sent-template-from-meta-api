import logging
import requests
from django.conf import settings
import threading
import time
from datetime import datetime

logger = logging.getLogger(__name__)

def upload_file_get_media_id(file_obj, media_type):
    url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}"
    }

    content_type_map = {
        "image": "image/jpeg",
        "video": "video/mp4",
        "document": "application/pdf"
    }
    content_type = content_type_map.get(media_type, "application/octet-stream")

    files = {
        'file': (file_obj.name, file_obj.read(), content_type),
        'messaging_product': (None, 'whatsapp')
    }

    logger.info(f"📤 Uploading {media_type}: {file_obj.name}")
    res = requests.post(url, headers=headers, files=files)
    logger.info(f"📤 Upload Status: {res.status_code} | Response: {res.text}")

    if res.status_code == 200:
        return res.json().get("id")
    else:
        logger.error(f"❌ Media Upload Failed: {res.text}")
        return None


def send_template_message_to_numbers(template_name, numbers, variables, language="en_US", media_payload=None):
    url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    for number in numbers:
        components = []

        if media_payload:
            media_type = media_payload["type"]
            media_id = media_payload["media_id"]
            components.append({
                "type": "header",
                "parameters": [{
                    "type": media_type,
                    media_type: {"id": media_id}
                }]
            })

        if variables:
            components.append({
                "type": "body",
                "parameters": [
                    {"type": "text", "text": variables.get(str(i + 1), "")}
                    for i in range(len(variables))
                ]
            })

        payload = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language},
                "components": components
            }
        }

        try:
            res = requests.post(url, headers=headers, json=payload)
            logger.info(f"[TEMPLATE] ✅ Sent to {number}: {res.status_code} {res.text}")
        except Exception as e:
            logger.error(f"[TEMPLATE] ❌ Failed to send to {number}: {str(e)}")

