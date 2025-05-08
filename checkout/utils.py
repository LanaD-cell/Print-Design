from cart.models import Cart

def get_or_create_cart(request):
    """Utility to get or create cart for authenticated or guest user."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart
