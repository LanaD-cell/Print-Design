from django.urls import path
from . import views
from webhooks import webhook

app_name = 'checkout'

urlpatterns = [
    path('summary/', views.order_summary, name='order_summary'),
    path(
        'checkout/', views.create_order, name='create_cart_order'
    ),
    path(
        'order_checkout/', views.checkout, name='order_checkout'
    ),
    path(
        'checkout/success/<session_id>',
        views.checkout_success_page,
        name='checkout_success_page'
    ),
    path(
        'webhook/',
        webhook,
        name='webhook'
    ),
]
