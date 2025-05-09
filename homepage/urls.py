from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'homepage'

handler404 = 'homepage.views.custom_404_view'
handler500 = 'homepage.views.custom_500_view'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('contact/', views.contact_view, name='contact'),
    path('contact_success/', views.contact_success_view, name='contact_success'),
]
