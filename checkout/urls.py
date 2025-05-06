from django.urls import path
from . import views
from webhooks import webhook

app_name = 'checkout'

urlpatterns = [
    path('summary/', views.order_summary, name='order_summary'),
    path('checkout/', views.create_order, name='create_cart_order'),
    path('success/', views.payment_success, name='payment_success'),
    path('webhook/', webhook, name='webhook'),
]
