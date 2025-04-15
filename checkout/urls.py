from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
        path('summary/', views.order_summary, name='order_summary'),
        path('checkout/', views.create_order, name='create_cart_order'),
        path('order_checkout/', views.checkout, name='order_checkout'),
]