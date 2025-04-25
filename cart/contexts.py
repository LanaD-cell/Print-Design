from decimal import Decimal
from django.conf import settings
from .models import Cart


def cart_contents(request):
    """ Create Cart contents for Cost and Delivery Calculations """

    cart = None  # Default to None

    # If the user is authenticated, fetch or create the user's cart
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart(user=request.user)
            cart.save()

    else:
        # For unauthenticated users, use the session to get the cart
        cart = request.session.get('cart', None)

        # If no cart exists in session, create an empty cart (or redirect to a login page if needed)
        if not cart:
            cart = {}  # Empty cart for unauthenticated users

    # If cart is valid, process the cart contents
    cart_items = cart.items.all() if cart and hasattr(cart, 'items') else []
    total = cart.total_price() if cart and hasattr(cart, 'total_price') else Decimal('0.00')

    # Product count (number of unique items in the cart)
    product_count = cart.items.count() if cart and hasattr(cart, 'items') else 0

    # Initialize delivery cost logic
    delivery = Decimal('0.00')

    # Delivery logic (if the cart total is below the free delivery threshold)
    if total < settings.FREE_DELIVERY_THRESHOLD:
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    # Grand total (including delivery)
    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }

    return context
