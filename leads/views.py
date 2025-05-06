from django.shortcuts import render, redirect
from .forms import LeadForm
from .models import Lead

def lead_capture(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.score = 50 if "@company.com" in lead.email else 30
            lead.save()
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'lead_form.html', {'form': form})

def lead_list(request):
    leads = Lead.objects.all().order_by('-timestamp')
    return render(request, 'lead_list.html', {'leads': leads})
