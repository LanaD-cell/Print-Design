from django.urls import path
from . import views
from checkout.views import checkout_success_page

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('checkout-success/<str:session_id>/', checkout_success_page, name='checkout_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
]
