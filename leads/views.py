from django.shortcuts import render, redirect
from .forms import LeadForm, LeadFilterForm
from .models import Lead
from .utils import send_email

def lead_create_view(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.compute_score_and_segment()
            lead.save()
            send_email(lead.email)  # Call with only the email
            return redirect('lead_success')
    else:
        form = LeadForm()
    return render(request, 'lead_form.html', {'form': form})

def lead_success_view(request):
    return render(request, 'lead_success.html')

def report_view(request):
    leads = Lead.objects.all()
    form = LeadFilterForm(request.GET)
    if form.is_valid():
        interest = form.cleaned_data.get('interest')
        min_score = form.cleaned_data.get('min_score')
        max_score = form.cleaned_data.get('max_score')

        if interest:
            leads = leads.filter(interest__icontains=interest)
        if min_score is not None:
            leads = leads.filter(score__gte=min_score)
        if max_score is not None:
            leads = leads.filter(score__lte=max_score)

    return render(request, 'report.html', {'leads': leads, 'form': form})
