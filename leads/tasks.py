import threading
import time
from .utils import send_whatsapp, upload_video_get_media_id
from django.conf import settings
import os

def schedule_followup_messages(phone, name):
    def task():
        try:
            video_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'whatsapp_ready.mp4')
            media_id = upload_video_get_media_id(video_path)

            if media_id:
                # After 15 minutes
                time.sleep(900)
                send_whatsapp(phone, media_id=media_id, name_param=name)

                # After 1 more hour (total 1h15m)
                time.sleep(2700)
                send_whatsapp(phone, media_id=media_id, name_param=name)
        except Exception as e:
            print(f"❌ Error in follow-up thread: {str(e)}")

    thread = threading.Thread(target=task)
    thread.start()
