from django.shortcuts import render, redirect, get_object_or_404
from .forms import LeadForm, LeadFilterForm
from .models import Lead
import pandas as pd
from django.http import HttpResponse

def lead_create_view(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.compute_score_and_segment()
            lead.save()
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

def lead_list(request):
    leads = Lead.objects.all()
    search_query = request.GET.get('search', '')
    interest_filter = request.GET.get('interest', '')

    if search_query:
        leads = leads.filter(name__icontains=search_query)
    if interest_filter:
        leads = leads.filter(interest=interest_filter)

    return render(request, 'lead_list.html', {'leads': leads})

def export_leads_csv(request):
    leads = Lead.objects.all().values()
    df = pd.DataFrame(leads)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=leads.csv'
    df.to_csv(path_or_buf=response, index=False)
    return response

# 💥 New delete view
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    return redirect('lead_list')
