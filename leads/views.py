from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from .models import Lead
from .forms import LeadForm, LeadFilterForm
from .tasks import send_email_task, send_whatsapp_task, send_followup_whatsapp_task
import pandas as pd

def lead_create_view(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.compute_score_and_segment()
            lead.save()

            send_email_task.delay(
                lead.email,
                "Thank You for Your Interest",
                "Thanks for your interest. Our team will follow up shortly."
            )

            if lead.phone:
                # Send first message immediately
                send_whatsapp_task.delay(lead.phone, lead.name)

                # Send second message after 15 minutes
                send_followup_whatsapp_task.apply_async(
                    args=[lead.phone, lead.name, 2],
                    countdown=900  # 15 minutes
                )

                # Send third message after 1 hour
                send_followup_whatsapp_task.apply_async(
                    args=[lead.phone, lead.name, 3],
                    countdown=3600  # 60 minutes
                )

            return redirect('lead_success')
    else:
        form = LeadForm()
    return render(request, 'lead_form.html', {'form': form})

'''
# Create a lead
def lead_create_view(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.compute_score_and_segment()
            lead.save()

            # Debugging the phone number
            # Inside lead_create_view
            if lead.phone:
                print(f"Sending WhatsApp message to {lead.phone}")  # Check phone number

            send_email_task.delay(
                lead.email,
                "Thank You for Your Interest",
                "Thanks for your interest. Our team will follow up shortly."
            )

            if lead.phone:
                send_whatsapp_task.delay(
                    lead.phone,
                    lead.name  # <- send name for the template
                ) 
                # Send WhatsApp message using the task  

            return redirect('lead_success')
    else:
        form = LeadForm()
    return render(request, 'lead_form.html', {'form': form})

'''

# Show all leads with search and pagination
def lead_list(request):
    leads = Lead.objects.all()
    query = request.GET.get('q')
    if query:
        leads = leads.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(segment__icontains=query)
        )
    paginator = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'lead_list.html', {'page_obj': page_obj})

# Delete a lead
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        lead.delete()
        return redirect('lead_list')
    return render(request, 'confirm_delete.html', {'lead': lead})

# Lead success page
def lead_success_view(request):
    return render(request, 'lead_success.html')

# Send WhatsApp message to a single lead
def send_whatsapp_message_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    # Inside send_whatsapp_message_view
    if lead.phone:
        send_whatsapp_task.delay(
            lead.phone,
            lead.name  # <- send name for the template
        )
    return redirect('lead_list')

# Report page
def report_view(request):
    leads = Lead.objects.all()
    form = LeadFilterForm(request.GET or None)
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

    paginator = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'report.html', {'page_obj': page_obj, 'form': form})

# CSV export
def export_leads_csv(request):
    leads = Lead.objects.all()
    interest = request.GET.get('interest')
    min_score = request.GET.get('min_score')
    max_score = request.GET.get('max_score')

    if interest:
        leads = leads.filter(interest__icontains=interest)
    if min_score:
        leads = leads.filter(score__gte=min_score)
    if max_score:
        leads = leads.filter(score__lte=max_score)

    df = pd.DataFrame(list(leads.values()))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=filtered_leads.csv'
    df.to_csv(path_or_buf=response, index=False)
    return response
