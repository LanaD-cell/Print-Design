from django.urls import path
from .views import( product_detail,
                   all_products,
                   terms,
                   main_nav,)


urlpatterns = [
    path('products/', all_products, name='products'),
    path('terms/', terms, name='terms'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('main-nav/', main_nav, name='main_nav'),
]
