from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]