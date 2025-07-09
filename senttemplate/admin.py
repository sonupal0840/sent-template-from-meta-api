from django.contrib import admin
from .models import MessageLog

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ("phone", "name", "template_type", "status", "timestamp")
    list_filter = ("status", "template_type")
    search_fields = ("phone", "name", "template_type")


