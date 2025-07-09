from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import MessageLog

class MessageLogTest(TestCase):
    def test_create_log(self):
        log = MessageLog.objects.create(
            phone="+911234567890",
            name="Test User",
            template_type="status_updated",
            status="sent"
        )
        self.assertEqual(log.phone, "+911234567890")
        self.assertEqual(log.status, "sent")
