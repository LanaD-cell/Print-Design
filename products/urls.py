from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.all_products, name='products'),  # Show all products
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Show product detail
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  # Show products by category
]
