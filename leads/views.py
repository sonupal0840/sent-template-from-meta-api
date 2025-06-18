from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Lead
from .forms import LeadForm, LeadFilterForm
from .utils import send_whatsapp, send_followup_whatsapp
import pandas as pd
import threading  # ✅ added

def lead_create_view(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.compute_score_and_segment()
            lead.save()

            # Send email
            send_mail(
                subject="Thank You for Your Interest",
                message="Thanks for your interest. Our team will follow up shortly.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[lead.email],
                fail_silently=False,
            )

            # Send WhatsApp
            if lead.phone:
                send_whatsapp(lead.phone, lead.name)

                # ✅ Delayed follow-ups using threading
                threading.Timer(300, send_followup_whatsapp, args=(lead.phone, lead.name, 2)).start()     # after 5 mins
                threading.Timer(3600, send_followup_whatsapp, args=(lead.phone, lead.name, 3)).start()    # after 1 hour

            return redirect('lead_success')
    else:
        form = LeadForm()
    return render(request, 'lead_form.html', {'form': form})


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


def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        lead.delete()
        return redirect('lead_list')
    return render(request, 'confirm_delete.html', {'lead': lead})


def lead_success_view(request):
    return render(request, 'lead_success.html')


def send_whatsapp_message_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if lead.phone:
        send_whatsapp(lead.phone, lead.name)
    return redirect('lead_list')


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


def privacy_view(request):
    return render(request, 'Privacy-policy.html')


def whatsapp_webhook_view(request):
    if request.method == 'GET':
        verify_token = settings.META_VERIFY_TOKEN
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == verify_token:
                return HttpResponse(challenge, status=200)
            else:
                return HttpResponse("Forbidden", status=403)
    return HttpResponse("Bad Request", status=400)
