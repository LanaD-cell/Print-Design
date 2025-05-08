from decimal import Decimal
from django.conf import settings
from .models import Cart

VAT_RATE = Decimal('0.19')

def cart_contents(request):
    """Create Cart contents for cost, VAT, and delivery calculations."""
    if not request.user.is_authenticated:
        return {}

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.all() if hasattr(cart, 'items') else []

    subtotal = cart.grand_total() if hasattr(cart, 'grand_total') else Decimal('0.00')
    vat = subtotal * VAT_RATE
    vat = vat.quantize(Decimal('0.01'))
    delivery = Decimal('5.00')
    grand_total = subtotal + vat + delivery
    grand_total = grand_total.quantize(Decimal('0.01'))

    stripe_public_key = settings.STRIPE_PUBLIC_KEY if hasattr(settings, 'STRIPE_PUBLIC_KEY') else None

    return {
        'cart_items': cart_items,
        'subtotal': subtotal.quantize(Decimal('0.01')),
        'vat': vat.quantize(Decimal('0.01')),
        'delivery': delivery.quantize(Decimal('0.01')),
        'grand_total': grand_total.quantize(Decimal('0.01')),
        'stripe_public_key': stripe_public_key,
    }
