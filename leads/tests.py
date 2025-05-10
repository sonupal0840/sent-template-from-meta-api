from django.test import TestCase
from .models import Lead
from django.core.exceptions import ValidationError

class LeadModelTest(TestCase):

    def test_create_lead(self):
        """Test that a lead can be created successfully."""
        lead = Lead.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="+12345678901",
            interest="I want to buy a product"
        )
        self.assertEqual(lead.name, "John Doe")
        self.assertEqual(lead.email, "john@example.com")
        self.assertEqual(lead.phone, "+12345678901")
        self.assertEqual(lead.interest, "I want to buy a product")
        self.assertEqual(lead.score, 50)  # Based on 'buy' in interest
        self.assertEqual(lead.segment, 'Hot')  # Based on score of 50

    def test_score_and_segment_calculation(self):
        """Test that the score and segment are correctly calculated."""
        lead = Lead.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            phone="+12345678902",
            interest="I'm interested in a demo"
        )
        # Score should be 30 based on the 'demo' keyword
        self.assertEqual(lead.score, 30)
        self.assertEqual(lead.segment, 'Warm')  # Based on score 30

        lead.interest = "I need more information"
        lead.save()  # Saving the updated lead
        # Score should be 10 based on the 'info' keyword
        self.assertEqual(lead.score, 10)
        self.assertEqual(lead.segment, 'Cold')  # Based on score 10

    def test_invalid_phone_number(self):
        """Test that an invalid phone number raises a ValidationError."""
        invalid_phone = "12345abc"  # Invalid phone number format
        lead = Lead(
            name="Test User",
            email="test@example.com",
            phone=invalid_phone,
            interest="Looking for a demo"
        )
        with self.assertRaises(ValidationError):
            lead.full_clean()  # This will trigger validation before saving

    def test_valid_phone_number(self):
        """Test that a valid phone number does not raise an error."""
        valid_phone = "+12345678901"
        lead = Lead(
            name="Test User",
            email="test@example.com",
            phone=valid_phone,
            interest="Looking for a demo"
        )
        try:
            lead.full_clean()  # Should not raise any exception
        except ValidationError:
            self.fail("Valid phone number raised ValidationError")

    def test_lead_str_method(self):
        """Test that the __str__ method returns the correct output."""
        lead = Lead.objects.create(
            name="Alice Cooper",
            email="alice@example.com",
            phone="+12345678903",
            interest="I want to buy"
        )
        self.assertEqual(str(lead), "Alice Cooper (Hot)")  # Expecting name and segment

