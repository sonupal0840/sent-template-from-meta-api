from django.urls import path
from . import views

urlpatterns = [
    path("trigger/", views.trigger_template_message, name="trigger_template_message"),
    path("get-templates/", views.get_templates_from_meta, name="get_templates_from_meta"),
    path("message-log/", views.message_log_report, name="message_log_report"),
    path("", views.automated_template_from_api, name="automated_template_from_api"),
]
