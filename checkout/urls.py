from django.urls import path
from webhooks import webhook

app_name = 'checkout'

urlpatterns = [
    path('webhook/', webhook, name='stripe_webhook'),
]
