import threading
import time
from .utils import send_whatsapp, upload_video_get_media_id
from django.conf import settings
import os
from django.utils.timezone import now, timedelta
from .models import MessageLog

def schedule_followup_messages(phone, name):
    try:
        video_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'whatsapp_ready.mp4')
        media_id = upload_video_get_media_id(video_path)

        if media_id:
            MessageLog.objects.create(
                phone=phone,
                name=name,
                message="Follow-up 1",
                template_type='followup1',
                status='pending',
                media_id=media_id,
                scheduled_for=now() + timedelta(minutes=15)
            )
            MessageLog.objects.create(
                phone=phone,
                name=name,
                message="Follow-up 2",
                template_type='followup2',
                status='pending',
                media_id=media_id,
                scheduled_for=now() + timedelta(hours=1, minutes=15)
            )
    except Exception as e:
        print(f"❌ Error scheduling follow-ups: {str(e)}")