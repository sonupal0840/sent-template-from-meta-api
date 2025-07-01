import requests
import json
import os
import logging
import threading
import time
from django.conf import settings
from .models import WhatsAppSession
from django.utils.timezone import now
from datetime import timedelta

logger = logging.getLogger(__name__)

def upload_video_get_media_id(file_path):
    if not os.path.exists(file_path):
        logger.error(f"❌ Video file not found: {file_path}")
        return None

    url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}"
    }

    with open(file_path, 'rb') as file_obj:
        files = {
            'file': (os.path.basename(file_path), file_obj, 'video/mp4'),
            'messaging_product': (None, 'whatsapp')
        }

        response = requests.post(url, headers=headers, files=files)
        logger.info(f"📤 Video upload response: {response.status_code} {response.text}")

        if response.status_code == 200:
            return response.json().get('id')
        return None


def send_whatsapp(phone_number, media_id=None, name_param=None):
    url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    template_data = {
        "name": "confirmation_video",  # ✅ your approved template
        "language": {"code": "en_US"},
        "components": []
    }

    if media_id:
        template_data["components"].append({
            "type": "header",
            "parameters": [{
                "type": "video",
                "video": {
                    "id": media_id
                }
            }]
        })

    name_text = name_param or "User"
    template_data["components"].append({
        "type": "body",
        "parameters": [{
            "type": "text",
            "text": name_text
        }]
    })

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": template_data
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        logger.info(f"✅ WhatsApp sent to {phone_number}: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"❌ Failed to send WhatsApp: {str(e)}")


def handle_first_time_message(phone_number, name="User"):
    session, created = WhatsAppSession.objects.get_or_create(phone=phone_number)

    if created or now() - session.last_message_at > timedelta(hours=24):
        video_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'whatsapp_ready.mp4')
        media_id = upload_video_get_media_id(video_path)
        if phone_number and media_id:
            send_whatsapp(phone_number, media_id=media_id, name_param=name)

            # ✅ schedule follow-up in background
            thread = threading.Thread(
                target=schedule_followups,
                args=(phone_number, name, media_id)
            )
            thread.start()

    session.last_message_at = now()
    session.save()


def schedule_followups(phone_number, name, media_id):
    try:
        logger.info(f"⏱ Waiting 15 min for follow-up to {phone_number}")
        time.sleep(900)  # 15 mins
        send_whatsapp(phone_number, media_id=media_id, name_param=name)
        logger.info(f"✅ 15-min follow-up sent to {phone_number}")

        time.sleep(2700)  # another 45 mins (total 1h)
        send_whatsapp(phone_number, media_id=media_id, name_param=name)
        logger.info(f"✅ 1-hour follow-up sent to {phone_number}")
    except Exception as e:
        logger.error(f"❌ Error in follow-up: {str(e)}")
