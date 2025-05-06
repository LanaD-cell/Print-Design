from decimal import Decimal
from django.conf import settings
from .models import Cart

VAT_RATE = Decimal('0.19')

def cart_contents(request):
    """Create Cart contents for cost, VAT, and delivery calculations."""

    cart = None

    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Get the items and calculate the subtotal
    cart_items = cart.items.all()
    subtotal = cart.total_price() if hasattr(cart, 'total_price') else Decimal('0.00')

    # VAT calculation
    vat = subtotal * VAT_RATE

    # Delivery logic
    if subtotal < settings.FREE_DELIVERY_THRESHOLD:
        delivery = settings.STANDARD_DELIVERY_COST
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - subtotal
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = Decimal('0.00')

    grand_total = subtotal + vat + delivery

    return {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'vat': vat,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
