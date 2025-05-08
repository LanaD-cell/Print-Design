from django.urls import path
from .views import (
    product_detail,
    all_products,
    terms,
    main_nav,
    manage_products,
    create_product,
    update_product,
    delete_product,
)

urlpatterns = [
    path('products/', all_products, name='products'),
    path('terms/', terms, name='terms'),
    path(
        'product/<int:product_id>/',
        product_detail, name='product_detail'
    ),
    path(
        'products/admin/manage-products/',
        manage_products, name='manage_products'
    ),
    path(
        'products/admin/products/create/',
        create_product, name='create_product'
    ),
    path(
        'products/admin/products/<int:pk>/edit/',
        update_product, name='update_product'
    ),
    path(
        'products/admin/products/<int:pk>/delete/',
        delete_product, name='delete_product'
    ),
    path('main-nav/', main_nav, name='main_nav'),
]
