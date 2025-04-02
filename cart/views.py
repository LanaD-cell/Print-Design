from django.shortcuts import render

# Create your views here.
def view_cart(request):
    """ View to return Cart """
    return render(request, 'cart/cart.html')
