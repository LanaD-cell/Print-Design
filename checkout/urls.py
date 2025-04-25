from django.urls import path
from . import views
from .webhooks import webhook

app_name = 'checkout'

urlpatterns = [
        path('summary/', views.order_summary, name='order_summary'),
        path('checkout/', views.create_order, name='create_cart_order'),
        path('order_checkout/', views.checkout, name='order_checkout'),
        path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
        path('payment/confirm', views.payment_confirm, name='payment_confirm'),
        path('wh/', webhook, name='webhooks'),
]