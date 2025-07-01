import requests
import json
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# ✅ Upload video and get media ID
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

# ✅ Send WhatsApp video template message
def send_whatsapp(phone_number, media_id=None, name_param=None):
    url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    template_data = {
        "name": "confirmation_video",  # ✅ Match exact approved template name
        "language": {"code": "en_US"},
        "components": []
    }

    # Add header component with video
    if media_id:
        template_data["components"].append({
            "type": "header",
            "parameters": [
                {
                    "type": "video",
                    "video": {
                        "id": media_id
                    }
                }
            ]
        })

    # Always add body parameter (fallback if missing)
    name_text = name_param or "User"
    template_data["components"].append({
        "type": "body",
        "parameters": [
            {
                "type": "text",
                "text": name_text
            }
        ]
    })

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": template_data
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"✅ WhatsApp sent to {phone_number}: {response.status_code} {response.text}")
        logger.info(f"✅ WhatsApp response: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"❌ Failed to send WhatsApp message: {str(e)}")
        print(f"❌ Error sending WhatsApp: {str(e)}")
# ____________________________________________________________________________



def handle_first_time_message(phone_number, name="User"):
    from .tasks import schedule_followup_messages

    # Trigger confirmation video + schedule next messages
    video_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'whatsapp_ready.mp4')
    media_id = upload_video_get_media_id(video_path)
    if phone_number and media_id:
        send_whatsapp(phone_number, media_id=media_id, name_param=name)
        schedule_followup_messages(phone_number, name)
