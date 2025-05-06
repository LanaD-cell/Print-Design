from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='cart_details'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/<order_number>/',
        views.payment_success,
        name='payment_success'
    ),
    path(
        'cancel/',
        views.payment_cancel,
        name='payment_cancel'
    ),
    path(
        'payment/confirm/',
        views.payment_confirm,
        name='payment_confirm'
    ),
]
