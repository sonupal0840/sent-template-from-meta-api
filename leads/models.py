from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    interest = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    segment = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return the lead's name and segment in the admin or any representation."""
        return f"{self.name} ({self.segment})"

    def compute_score_and_segment(self):
        """
        Computes the score based on interest keywords and assigns the segment.
        Keywords:
        - "buy"  → +50 points
        - "demo" → +30 points
        - "info" → +10 points

        Segments:
        - Hot   (score ≥ 50)
        - Warm  (30 ≤ score < 50)
        - Cold  (score < 30)
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
        """Custom phone number validation."""
        phone_pattern = re.compile(r'^\+\d{10,15}$')
        if not phone_pattern.match(self.phone):
            raise ValidationError("Phone number must be in the format +1234567890 (10–15 digits).")

    def save(self, *args, **kwargs):
        """Override save to auto-calculate score and segment before saving."""
        self.compute_score_and_segment()
        super().save(*args, **kwargs)
