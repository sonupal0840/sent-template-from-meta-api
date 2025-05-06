from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'interest']

class LeadFilterForm(forms.Form):
    interest = forms.CharField(required=False, label='Interest Contains')
    min_score = forms.IntegerField(required=False, label='Min Score')
    max_score = forms.IntegerField(required=False, label='Max Score')
