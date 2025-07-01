from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from datetime import timedelta

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    interest = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    segment = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Returns a string representation with name and segment."""
        return f"{self.name} ({self.segment})"

    def compute_score_and_segment(self):
        """
        Assigns score based on keywords in interest.
        Score Rules:
        - 'buy'  → +50
        - 'demo' → +30
        - 'info' → +10

        Segment Assignment:
        - Hot  : score ≥ 50
        - Warm : 30 ≤ score < 50
        - Cold : score < 30
        """
        score = 0
        interest_lower = self.interest.lower()

        if "buy" in interest_lower:
            score += 50
        if "demo" in interest_lower:
            score += 30
        if "info" in interest_lower:
            score += 10

        self.score = score

        if score >= 50:
            self.segment = 'Hot'
        elif 30 <= score < 50:
            self.segment = 'Warm'
        else:
            self.segment = 'Cold'

    def clean(self):
        """
        Validates phone number format:
        Must start with '+' followed by 10–15 digits.
        """
        phone_pattern = re.compile(r'^\+\d{10,15}$')
        if not phone_pattern.match(self.phone):
            raise ValidationError("Phone number must be in the format +1234567890 (10–15 digits).")

    def save(self, *args, **kwargs):
        """Automatically compute score and segment on save."""
        self.compute_score_and_segment()
        super().save(*args, **kwargs)


class WhatsAppSession(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    last_message_at = models.DateTimeField(auto_now=True)

    def is_session_active(self):
        """
        Returns True if the user has sent a message within the last 24 hours.
        """
        return timezone.now() - self.last_message_at < timedelta(hours=24)

    def __str__(self):
        return f"{self.phone} - Active: {self.is_session_active()}"
