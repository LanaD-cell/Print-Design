from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
        path('summary/', views.order_summary, name='order_summary'),
        path('checkout/', views.create_order, name='create_cart_order'),
        path('order_checkout/', views.checkout, name='order_checkout'),
        path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
        path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
        path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
        path('payment-success/<order_number>/', views.payment_success, name='payment_success'),
        path('payment/confirm/', views.payment_confirm, name='payment_confirm'),
]