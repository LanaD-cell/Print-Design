from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required


@login_required
# View to return Cart
def view_cart(request):
    """ View to return Cart """
    cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'cart/cart.html', {'cart': cart})


# This view is for adding the product to the cart
def add_to_cart(request, product_id):
    """ Add a product to the cart """
    product = get_object_or_404(Product, id=product_id)

    # Get quantity/size from the form, default to 1 if not provided
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('product_size')

    # Get the user's cart or create one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # If the product requires a size but no size is selected, handle this error
    if product.has_sizes and not size:
        return redirect('product_detail', product_id=product.id)

    # Add the product to the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
    )
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()
    cart.save()

    # Redirect to the appropriate page (usually the cart or the previous page)
    redirect_url = request.POST.get('redirect_url', 'view_cart')
    return redirect(redirect_url)
