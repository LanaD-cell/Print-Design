from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('account/', include('allauth.urls')),
    path('', include('homepage.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('login/', include('django.contrib.auth.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
