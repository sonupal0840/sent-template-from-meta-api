from django.contrib import admin
from .models import Lead, WhatsAppSession,MessageLog

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')

@admin.register(WhatsAppSession)
class WhatsAppSessionAdmin(admin.ModelAdmin):
    list_display = ('phone', 'last_message_at', 'is_session_active')
    search_fields = ['phone']
    list_filter = ['last_message_at']

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('phone', 'template_type', 'status', 'timestamp')
    search_fields = ['phone', 'name']
    list_filter = ['template_type', 'status', 'timestamp']