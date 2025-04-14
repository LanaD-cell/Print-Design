from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='cart_details'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
]
