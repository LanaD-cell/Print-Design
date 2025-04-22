from decimal import Decimal
from django.conf import settings
from .models import Cart


def cart_contents(request):
    """ Create Cart contents for Cost and Delivery Calculations """

    # Make sure user is authenticated to access cart
    if request.user.is_authenticated:
        # Get the user's cart, or create one if it doesn't exist
        cart = Cart.objects.get(user=request.user)
    else:

        cart = request.session.get('cart', {})

    # Calculate the total and items count
    cart_items = cart.items.all() if cart and hasattr(cart, 'items') else []
    total = cart.total_price() if cart and hasattr(
        cart, 'total_price') else Decimal('0.00')

    # Product count (number of unique items in the cart)
    product_count = cart.items.count() if cart and hasattr(
        cart, 'items') else 0

    # Delivery logic
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
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
