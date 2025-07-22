from django.apps import AppConfig


from .utils import send_whatsapp

class LeadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leads'

    def ready(self):
        from .models import MessageLog
        import threading, time
        from django.utils.timezone import now
        from django.db import connection
        def process_scheduled_followups():
            while True:
                try:
                    if connection.connection is not None:
                        connection.connection.ping(True)

                    due_messages = MessageLog.objects.filter(
                        status='pending',
                        scheduled_for__lte=now()
                    )
                    for msg in due_messages:
                        send_whatsapp(phone=msg.phone, media_id=msg.media_id, name_param=msg.name)
                        msg.status = 'sent'
                        msg.save()

                    time.sleep(60)
                except Exception as e:
                    print(f"❌ Scheduler error: {str(e)}")
                    time.sleep(60)

        threading.Thread(target=process_scheduled_followups, daemon=True).start()