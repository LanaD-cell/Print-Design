from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

# This view is for rendering a list of all products
def all_products(request):
    """ View to show all products, including search and filter by ID or category """

    # Get the product ID from the request (if any)
    product_id = request.GET.get('product_id', None)

    # Get the category filter (if any)
    category_id = request.GET.get('category_id', None)

    # Initialize the product query
    products = Product.objects.all()  # Default to show all products

    # Filter by product ID if provided
    if product_id:
        products = products.filter(id=product_id)

    # Filter by category ID if provided
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)

# This view is for displaying individual product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

# This view is for displaying products by category
def category_detail(request, category_id):
    """ View to show products in a specific category using the same template as all products """
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'products': products,
        'category': category,
    }

    return render(request, 'products/products.html', context)
