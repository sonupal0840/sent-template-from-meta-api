from django.db import models
from django.utils import timezone

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    interest = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    segment = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)  # Timestamp field for when the lead is created

    def __str__(self):
        """Return the lead's name and segment in the admin or any representation."""
        return f"{self.name} ({self.segment})"

    def compute_score_and_segment(self):
        """
        Computes the score based on interest keywords and assigns the segment based on the score.
        Score categories:
        - "buy" = +50 points
        - "demo" = +30 points
        - "info" = +10 points
        
        Segment is assigned as:
        - 'Hot' if score >= 50
        - 'Warm' if score is between 30 and 49
        - 'Cold' if score < 30
        """
        score = 0
        interest_lower = self.interest.lower()  # Convert to lowercase for case-insensitive matching
        
        # Scoring based on interest keywords
        if "buy" in interest_lower:
            score += 50
        if "demo" in interest_lower:
            score += 30
        if "info" in interest_lower:
            score += 10

        # Update the score and assign the segment
        self.score = score
        
        if score >= 50:
            self.segment = 'Hot'
        elif 30 <= score < 50:
            self.segment = 'Warm'
        else:
            self.segment = 'Cold'

    def save(self, *args, **kwargs):
        """
        Override the save method to compute score and segment before saving the lead object.
        """
        # Ensure score and segment are computed before saving the object
        self.compute_score_and_segment()  
        super().save(*args, **kwargs)
