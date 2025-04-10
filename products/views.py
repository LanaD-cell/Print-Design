from django.shortcuts import render, get_object_or_404
from .models import (Product,
                    Category,
                    ProductSize,
                    QuantityOption,
                    )
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



def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'products/product_detail.html', {'category': category})


# This view is for displaying individual product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Fetch all available sizes and quantity options
    sizes = product.product_sizes_set.all()
    quantity_options = product.quantity_options_set.all()

    # Initialize default selected values (None)
    selected_size = None
    selected_quantity = None
    selected_services = []
    selected_delivery = None
    total_price = 0.00

    # Check if the form is submitted
    if request.method == 'POST':
        selected_size = request.POST.get('size')
        selected_quantity = request.POST.get('quantity')
        selected_services = request.POST.getlist('additional_services')  # Handles multiple services
        selected_delivery = request.POST.get('delivery_option')

        # Get the price for the selected size and quantity
        size_obj = ProductSize.objects.filter(product=product, size=selected_size).first()
        quantity_obj = QuantityOption.objects.filter(product=product, quantity=int(selected_quantity)).first()

        # Calculate the total price based on selected size and quantity
        if size_obj and quantity_obj:
            total_price = quantity_obj.price  # Add more logic if needed for services or delivery

        # Optionally, add additional service prices to the total price
        for service in selected_services:
            # For simplicity, let's assume we just add a fixed price per service.
            if service == "Design Service":
                total_price += 40.00

        # Add delivery cost to the total price
        # based on the selected delivery option
        if selected_delivery == "Priority Delivery":
            total_price += 15.00
        elif selected_delivery == "Express Delivery":
            total_price += 25.00
        else:
            total_price += 0.00  # Standard Delivery

    context = {
        'product': product,
        'sizes': sizes,
        'quantity_options': quantity_options,
        'selected_size': selected_size,
        'selected_quantity': selected_quantity,
        'selected_services': selected_services,
        'selected_delivery': selected_delivery,
        'total_price': total_price,
    }

    return render(request, 'products/product_detail.html', context)

def terms(request):
    return render(request, 'terms.html')

def calculate_price(request, product_id):
    product = Product.objects.get(id=product_id)
    selected_size = request.POST.get('product_size')
    selected_quantity = int(request.POST.get('product_quantity'))

    quantity_option = product.quantity_options.filter(
        product_size__size=selected_size,
        quantity=selected_quantity
    ).first()

    if quantity_option:
        unit_price = quantity_option.price
        total_price = unit_price * selected_quantity
    else:
        total_price = product.price * selected_quantity

    return total_price

def main_nav(request):
    return render(request, 'main-nav.html')