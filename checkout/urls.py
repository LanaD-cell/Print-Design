from django.urls import path
from . import views
from webhooks import webhook

app_name = 'checkout'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/', webhook, name='stripe_webhook'),
]
