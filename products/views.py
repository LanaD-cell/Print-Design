from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

def product_list(request):
    # You can apply filters if necessary
    products = Product.objects.select_related('Category').all()
    return render(request, 'main-nav.html', {'products': products})

def all_products(request):
    """ View to show all products, including search and filter by ID """
    # Get the product ID from the request
    product_id = request.GET.get('product_id', None)

    # Initialize the product query
    products = Product.objects.all()  # Default to show all products

    # Filter products by ID if it's provided in the query string
    if product_id:
        try:
            products = Product.objects.filter(id=product_id)  # Filter by ID
        except Product.DoesNotExist:
            products = Product.objects.none()  # Return empty queryset if no matching product

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)

def category_detail(request, category_id):
    """ View to show products in a specific category using the same template as all products """
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'products': products,
        'category': category,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

