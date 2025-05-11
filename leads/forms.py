from django import forms
from .models import Lead




from django.core.exceptions import ValidationError

def validate_phone_number(value):
    if not value.startswith('+'):  # Check if country code is included
        raise ValidationError('Phone number must include the country code.')


class LeadForm(forms.ModelForm):
    phone = forms.CharField(required=False)

    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'interest']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone (e.g. +917000000000)'}),
            'interest': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Interest'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip().replace(' ', '')

        if phone and not phone.startswith('+'):
            phone = '+91' + phone  # Auto prefix if not present

        # Final validation
        if not phone.startswith('+91') or not phone[1:].isdigit():
            raise forms.ValidationError("Phone number must be in correct format (e.g. +917000000000)")

        return phone


class LeadFilterForm(forms.Form):
    interest = forms.CharField(
        required=False,
        label='Interest',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search Interest'})
    )
    min_score = forms.IntegerField(
        required=False,
        label='Min Score',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Score'})
    )
    max_score = forms.IntegerField(
        required=False,
        label='Max Score',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Score'})
    )