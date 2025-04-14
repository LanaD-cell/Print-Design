from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
        path('checkout/', views.create_order, name='create_cart_order'),
        path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
]