from django.contrib import admin
from .models import Lead, WhatsAppSession

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'score', 'segment')

@admin.register(WhatsAppSession)
class WhatsAppSessionAdmin(admin.ModelAdmin):
    list_display = ('phone', 'last_message_at')
