from django.urls import path
from .views import handle_whatsapp_message, success_view

urlpatterns = [
    path('whatsapp-webhook/', handle_whatsapp_message, name='whatsapp_webhook'),
    path('success/', success_view, name='success'),
    # Add other URL patterns as needed
]