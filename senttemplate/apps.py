from datetime import datetime, time, timedelta
from django.apps import AppConfig

class SenttemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'senttemplate'

#     def ready(self):
#         from django_q.models import Schedule
#         from django_q.tasks import schedule

#         if not Schedule.objects.filter(name='daily-whatsapp-task').exists():
#             now = datetime.now()
#             run_time = datetime.combine(now.date(), time(20, 35))  # 8:30 PM today

#             if now > run_time:
#                 # Agar aaj 8:30 PM beet chuka hai to kal ka 8:30 PM schedule karo
#                 run_time += timedelta(days=1)

#             schedule(
#                 'senttemplate.tasks.fetch_contacts_and_send_messages',
#                 name='daily-whatsapp-task',
#                 schedule_type=Schedule.DAILY,
#                 repeats=-1,
#                 next_run=run_time.strftime('%Y-%m-%d %H:%M:%S'),
#             )
# # from senttemplate.tasks import fetch_contacts_and_send_messages
# # fetch_contacts_and_send_messages()

