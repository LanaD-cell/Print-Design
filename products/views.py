from django.shortcuts import render
from .models import Product


def all_products(request):
    """ View to show all products, include search and sorting """
    products = Product.objects.all()
    print(products)
    context = {
        'products':products,
    }

    return render(request, 'products/products.html', context)
