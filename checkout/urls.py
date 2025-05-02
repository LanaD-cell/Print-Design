from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
        path('summary/', views.order_summary, name='order_summary'),
        path('checkout/', views.create_order, name='create_cart_order'),
        path('order_checkout/', views.checkout, name='order_checkout'),
        path('success/<session_id>', views.checkout_success, name='checkout_success_page'),
        path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
        path('payment-success/<order_number>/', views.payment_success, name='payment_success'),
        path('payment/confirm/', views.payment_confirm, name='payment_confirm'),
]