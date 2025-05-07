from decimal import Decimal
from django.conf import settings
from .models import Cart

VAT_RATE = Decimal('0.19')

def cart_contents(request):
    """Create Cart contents for cost, VAT, and delivery calculations."""

    # Check if the user is authenticated first
    if not request.user.is_authenticated:
        # If the user is not authenticated, return empty context instead of redirecting
        return {}

    # Attempt to get the user's cart or create a new one if it doesn't exist
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Safely get cart items
    cart_items = cart.items.all() if hasattr(cart, 'items') else []

    # Calculate subtotal - check if 'grand_total' exists on the cart object
    subtotal = cart.grand_total() if hasattr(cart, 'grand_total') else Decimal('0.00')

    # VAT calculation
    vat = subtotal * VAT_RATE

    # Delivery cost
    delivery = Decimal('5.00')

    # Grand total calculation
    grand_total = subtotal + vat + delivery

    # Stripe public key from settings
    stripe_public_key = settings.STRIPE_PUBLIC_KEY if hasattr(settings, 'STRIPE_PUBLIC_KEY') else None

    return {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'vat': vat,
        'delivery': delivery,
        'grand_total': grand_total,
        'stripe_public_key': stripe_public_key,
    }
