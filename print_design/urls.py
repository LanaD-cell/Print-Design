from django.contrib import admin
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from print_design.sitemaps import sitemaps
from django.conf.urls.static import static
from django.urls import path, include
from homepage.views import (
    CustomLoginView,
    login_success,
    logout_view,
    logout_success
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='sitemap'
    ),
    path('summernote/', include('django_summernote.urls')),
    path(
        'signup/',
        lambda request: redirect('/account/signup/'),
        name='signup'
    ),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('login-success/', login_success, name='login-success'),
    path('logout/', logout_view, name='logout'),
    path('logout-success/', logout_success, name='logout-success'),
    path('account/', include('allauth.urls')),
    path('', include('homepage.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
