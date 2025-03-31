from django.shortcuts import render, get_object_or_404
from .models import Product


def all_products(request):
    """ View to show all products, include search and sorting """
    products = Product.objects.all()
    print(products)
    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ View to show individual product details """
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
