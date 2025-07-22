from django.core.management.base import BaseCommand
from django_q.models import Schedule

class Command(BaseCommand):
    help = "Create a scheduled task to send WhatsApp messages daily at 8:30 PM"

    def handle(self, *args, **kwargs):
        if not Schedule.objects.filter(name="daily-whatsapp-task").exists():
            Schedule.objects.create(
                name="daily-whatsapp-task",
                func="senttemplate.tasks.send_daily_message",
                schedule_type=Schedule.DAILY,
                repeats=-1,
                next_run="20:30"  # 8:30 PM
            )
            self.stdout.write(self.style.SUCCESS("Scheduled task created."))
        else:
            self.stdout.write(self.style.WARNING("Task already exists."))
