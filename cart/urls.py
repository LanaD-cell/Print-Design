from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('login/', LoginView.as_view(), name='login'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_bag'),
    path('adjust/<item_id>/', views.adjust_cart, name='adjust_bag'),
    path('remove/<item_id>/', views.remove_from_cart, name='remove_from_bag'),
    path('account/login/', auth_views.LoginView.as_view(), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
]