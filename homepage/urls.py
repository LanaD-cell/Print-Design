from django.urls import path
from django.conf.urls import handler404, handler500
from django.contrib.auth import views as auth_views
from . import views

handler404 = '.views.custom_404_view'
handler500 = '.views.custom_500_view'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('facebook/', views.facebook_mockup, name='facebook_mockup'),
]
