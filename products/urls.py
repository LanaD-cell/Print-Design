from django.urls import path
from . import views
from .views import product_detail

urlpatterns = [
    path('products/', views.all_products, name='products'),
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),

]
