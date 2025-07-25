from django.db import models
from django.utils import timezone


# Create your models here.
class MessageLog(models.Model):
    MESSAGE_TYPES = [
        ('initial', 'Initial'),
        ('followup1', '15-min Follow-up'),
        ('followup2', '1-hour Follow-up'),
        ('status_updated', 'Status Updated') 
    ]

    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True)
    template_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    status = models.CharField(max_length=10)  # sent or failed
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.phone} - {self.template_type} - {self.status}"
