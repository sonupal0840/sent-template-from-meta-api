from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_create_view, name='home'),
    path('success/', views.lead_success_view, name='lead_success'),
    path('report/', views.report_view, name='report'),
    path('export-leads-csv/', views.export_leads_csv, name='export_leads_csv'),
    path('leads/', views.lead_list, name='lead_list'),  # added for WhatsApp reply list
    path('delete/<int:lead_id>/', views.delete_lead, name='delete_lead'),
]
