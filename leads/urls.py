from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_capture, name='lead_capture'),
    path('leads/', views.lead_list, name='lead_list'),
]
