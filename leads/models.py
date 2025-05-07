from django.db import models
from django.utils import timezone

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    interest = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    segment = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)  # New field

    def __str__(self):
        return self.name

    def compute_score_and_segment(self):
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
