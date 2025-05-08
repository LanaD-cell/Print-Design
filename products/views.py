from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Product, Category, ProductSize, QuantityOption
from .forms import ProductForm
import json
from django.conf import settings


def all_products(request):
    """ View to show all products,
    including search and filter by ID or category """
    product_id = request.GET.get('product_id', None)
    category_id = request.GET.get('category_id', None)
    products = Product.objects.all()

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

        if product_id:
            products = products.filter(id=product_id)

        if category_id:
            products = products.filter(category_id=category_id)

    if not products.exists():
        messages.error(
            request, 'No products found matching your search criteria.')

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(
        request, 'products/product_detail.html', {'category': category})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sizes = product.product_sizes_set.all()
    quantity_options = product.quantity_options_set.all()

    selected_size = None
    selected_quantity = None
    selected_services = []
    selected_delivery = None
    total_price = 0.00

    if request.method == 'POST':
        selected_size = request.POST.get('size')
        selected_quantity = request.POST.get('quantity')
        selected_services = request.POST.getlist('additional_services')
        selected_delivery = request.POST.get('delivery_option')

        size_obj = ProductSize.objects.filter(
            product=product, size=selected_size).first()
        quantity_obj = QuantityOption.objects.filter(
            product=product, quantity=int(selected_quantity)).first()

        if size_obj and quantity_obj:
            total_price = quantity_obj.price

        for service in selected_services:
            if service == "Design Service":
                total_price += 40.00

        if selected_delivery == "Priority Delivery":
            total_price += 15.00
        elif selected_delivery == "Express Delivery":
            total_price += 25.00
        else:
            total_price += 0.00

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
    """ Renders the terms and conditions when
    radio button is clicked on the contact form """
    return render(request, 'terms.html')


def calculate_price(request, product_id):
    """ Calculate the total price, either as
    a set price for quantity or unit price """
    product = Product.objects.get(id=product_id)
    selected_size = request.POST.get('product_size')
    selected_quantity = int(request.POST.get('product_quantity'))

    quantity_option = product.quantity_options.filter(
        product_size__size=selected_size, quantity=selected_quantity).first()

    if quantity_option:
        unit_price = quantity_option.price
        total_price = unit_price * selected_quantity
    else:
        total_price = product.price * selected_quantity

    return total_price


def main_nav(request):
    return render(request, 'main-nav.html')


@user_passes_test(lambda u: u.is_superuser)
def manage_products(request):
    products = Product.objects.all()
    return render(
        request, 'admin/manage_products.html', {'products': products})


@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('manage_products')
    return render(
        request, 'products/admin/confirm_delete.html', {'product': product})
