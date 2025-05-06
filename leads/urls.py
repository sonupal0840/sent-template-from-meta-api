from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_create_view, name='home'),
    path('success/', views.lead_success_view, name='lead_success'),
    path('report/', views.report_view, name='report'),
]
