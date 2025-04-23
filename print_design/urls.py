from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path, include
from checkout import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('registration/signup/', views.signup_view, name='account_signup'),
    path('registration/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='custom_login'),
    path('account/', include('allauth.urls')),
    path('', include('homepage.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls', namespace='checkout')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
