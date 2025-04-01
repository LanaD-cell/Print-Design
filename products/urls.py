from django.urls import path
from .views import( product_detail,
                   all_products,
                   category_detail,
                   terms_and_conditions)


urlpatterns = [
    path('products/', all_products, name='products'),
    path('terms/', terms_and_conditions, name='terms'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
]
