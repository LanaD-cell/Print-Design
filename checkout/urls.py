from django.urls import path
from . import views
from .webhooks import webhook

app_name = 'checkout'

urlpatterns = [
        path('summary/', views.order_summary, name='order_summary'),
        path('checkout/', views.create_order, name='create_cart_order'),
        path('order_checkout/', views.checkout, name='order_checkout'),
        path('checkout/success/<session_id>', views.checkout_success_page, name='checkout_success_page'),
        path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
        path('payment-success/<order_number>/', views.payment_success, name='payment_success'),
        path('payment/confirm/', views.payment_confirm, name='payment_confirm'),
        path('webhook/', webhook, name='webhook'),
]