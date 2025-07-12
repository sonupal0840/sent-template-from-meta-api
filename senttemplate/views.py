import json
import logging
import os
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from threading import Thread
from .utils import upload_file_get_media_id, send_template_message_to_numbers
from senttemplate.models import MessageLog

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def trigger_template_message(request):
    try:
        data = request.POST if request.content_type.startswith("multipart") else json.loads(request.body)

        template_name = data.get("template_name")
        language = data.get("language", "en_US")
        media_type = data.get("media_type")
        variables = json.loads(data.get("variables", "{}")) if isinstance(data.get("variables"), str) else data.get("variables", {})
        numbers = json.loads(data.get("numbers", "[]")) if isinstance(data.get("numbers"), str) else data.get("numbers", [])

        if not template_name or not numbers:
            return JsonResponse({"error": "Missing template or numbers"}, status=400)

        media_payload = None
        media_file = request.FILES.get("media_file") if hasattr(request, 'FILES') else None
        if media_file and media_type:
            media_id = upload_file_get_media_id(media_file, media_type)
            if media_id:
                media_payload = {"type": media_type, "media_id": media_id}

        filtered_numbers = []
        filtered_variables = {}

        for number in numbers:
            if template_name == "status_updated":
                already_sent = MessageLog.objects.filter(
                    phone=number,
                    template_type=template_name,
                    status="sent"
                ).exists()
                if already_sent:
                    continue

            filtered_numbers.append(number)
            filtered_variables[number] = variables.get(number, {"1": "User"})

        def send_to_all():
            for phone in filtered_numbers:
                try:
                    send_template_message_to_numbers(
                        template_name=template_name,
                        numbers=[phone],
                        variables=filtered_variables.get(phone, {"1": "User"}),
                        language=language,
                        media_payload=media_payload
                    )
                    MessageLog.objects.create(
                        phone=phone,
                        name=filtered_variables.get(phone, {}).get("1", ""),
                        template_type=template_name,
                        status='sent'
                    )
                except Exception as e:
                    logger.error(f"❌ Failed to send to {phone}: {str(e)}")
                    MessageLog.objects.create(
                        phone=phone,
                        name=filtered_variables.get(phone, {}).get("1", ""),
                        template_type=template_name,
                        status='failed'
                    )

        if filtered_numbers:
            Thread(target=send_to_all).start()
            return JsonResponse({"status": f"Started sending to {len(filtered_numbers)} numbers"}, status=200)
        else:
            return JsonResponse({"status": "No new numbers to send"}, status=200)

    except Exception as e:
        logger.exception("Template sending error")
        return JsonResponse({"error": str(e)}, status=500)


def get_templates_from_meta(request):
    url = f"https://graph.facebook.com/v19.0/{settings.META_WABA_ID}/message_templates"
    headers = {"Authorization": f"Bearer {settings.META_ACCESS_TOKEN}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        templates = [tmpl['name'] for tmpl in res.json().get('data', [])]
        return JsonResponse({'templates': templates})
    return JsonResponse({'error': 'Failed to fetch templates'}, status=400)


def automated_template_from_api(request):
    try:
        api_url = "https://callapi.sherlockslife.com/api/Values/contacts/"  # Replace with actual
        response = requests.get(api_url, timeout=10)

        if response.status_code != 200:
            return JsonResponse({"error": "Failed to fetch contacts"}, status=400)

        contacts = response.json()
        print(contacts)
        # contacts = [{'phone':7000454350,'name':'sonu'}]
        if not contacts:
            return JsonResponse({"error": "No contacts found"}, status=400)

        image_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'rejected.jpg')
        if not os.path.exists(image_path):
            return JsonResponse({"error": "Image file not found"}, status=400)

        with open(image_path, 'rb') as image_file:
            media_id = upload_file_get_media_id(image_file, media_type='image')

        if not media_id:
            return JsonResponse({"error": "Failed to upload image"}, status=500)

        numbers = []
        variables_dict = {}

        for contact in contacts:
            phone = contact.get("phone")
            name = contact.get("name", "User")
            if not phone:
                continue

            already_sent = MessageLog.objects.filter(
                phone=phone, template_type='status_updated', status='sent'
            ).exists()
            if already_sent:
                continue

            numbers.append(phone)
            variables_dict[phone] = {"1": name}

        def send_to_all():
            for phone in numbers:
                variables = variables_dict.get(phone, {"1": "User"})
                try:
                    send_template_message_to_numbers(
                        template_name='status_updated',
                        numbers=[phone],
                        variables=variables,
                        language="en_US",
                        media_payload={"type": "image", "media_id": media_id}
                    )
                    MessageLog.objects.create(
                        phone=phone,
                        name=variables.get("1", "User"),
                        template_type='status_updated',
                        status='sent'
                    )
                except Exception as e:
                    logger.error(f"❌ Failed to send to {phone}: {str(e)}")
                    MessageLog.objects.create(
                        phone=phone,
                        name=variables.get("1", "User"),
                        template_type='status_updated',
                        status='failed'
                    )

        if numbers:
            Thread(target=send_to_all).start()
            return JsonResponse({"status": f"Started sending to {len(numbers)} new contacts"}, status=200)
        else:
            return JsonResponse({"status": "No new contacts to send"}, status=200)

    except Exception as e:
        logger.exception("❌ Error in automated_template_from_api")
        return JsonResponse({"error": str(e)}, status=500)
