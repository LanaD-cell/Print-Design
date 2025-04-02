from django.shortcuts import render, get_object_or_404
from .models import Product, Category
import json
from django.conf import settings

# This view is for rendering a list of all products
def all_products(request):
    """ View to show all products, including search and filter by ID or category """

    # Get the product ID from the request (if any)
    product_id = request.GET.get('product_id', None)

    # Get the category filter (if any)
    category_id = request.GET.get('category_id', None)

    # Initialize the product query
    products = Product.objects.all()  # Default to show all products

    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)



    # Filter by product ID if provided
        if product_id:
            products = products.filter(id=product_id)

    # Filter by category ID if provided
        if category_id:
            products = products.filter(category_id=category_id)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'current_sorting': current_sorting,

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

def terms_and_conditions(request):
    return render(request, 'terms.html')

def main_nav(request):
    """ View to return main navigation with product data for modal """
    json_file_path = settings.BASE_DIR / 'products.json'

    with open(json_file_path) as f:
        products = json.load(f)

    return render(request, 'includes/main-nav.html', {'products': products})