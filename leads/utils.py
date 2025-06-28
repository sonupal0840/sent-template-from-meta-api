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






'''def upload_video_get_media_id(file_path_str):
    url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}"
    }
    with open(file_path_str, 'rb') as file_obj:
        files = {
            'file': (file_path_str.split('/')[-1], file_obj, 'video/mp4'),
            'messaging_product': (None, 'whatsapp')
        }
        response = requests.post(url, headers=headers, files=files)
        print("Upload response:", response.status_code, response.text)
        data = response.json()
        return data.get('id')


def send_whatsapp(phone_number, name, media_id=None):
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
            "name": "confirmation_video",  # Template name with video header
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "video",
                            "video": {
                                "id": media_id
                            }
                        }
                    ]
                },
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
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"WhatsApp sent to {phone_number}: {response.text}")
'''


# __________________________________________________________________________________
# import requests
# import json
# from django.conf import settings
# import logging

# logger = logging.getLogger(__name__)

# def send_whatsapp(phone_number, name):
#     _send_whatsapp(phone_number, name)  # Directly send name as template variable

# def send_followup_whatsapp(phone_number, name, step):
#     message_suffix = {
#         2: "Here’s some more info you might find useful.",
#         3: "Final follow-up! Feel free to reply if you have any questions."
#     }
#     followup_text = f"{name}, {message_suffix.get(step, '')}"
#     _send_whatsapp(phone_number, followup_text)

# def _send_whatsapp(phone_number, _unused=None):  # body_text not needed
#     url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/messages"

#     headers = {
#         "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "messaging_product": "whatsapp",
#         "to": phone_number,
#         "type": "template",
#         "template": {
#             "name": "hello_world",  # This template must not expect any parameters
#             "language": {
#                 "code": "en_US"
#             }
#         }
#     }

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(payload))
#         logger.info(f"WhatsApp Response ({response.status_code}): {response.text}")
#         print(f"WhatsApp sent to {phone_number}: {response.text}")
#     except Exception as e:
#         logger.error(f"Failed to send WhatsApp message: {str(e)}")
#         print(f"Error sending WhatsApp to {phone_number}: {str(e)}")
