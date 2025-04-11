from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='cart_details'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.create_order, name='create_cart_order'),
]
