from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from checkout.views import get_or_create_cart
from django.contrib import messages
from checkout.models import Order, OrderLineItem
from .models import Product, Cart, CartItem
from django.conf import settings
import uuid
import stripe
import re
from decimal import Decimal
import json

stripe.api_key = settings.STRIPE_SECRET_KEY


def view_cart(request):
    try:
        # Get the user's cart, raise an exception if not found
        cart = Cart.objects.get(user=request.user)

        # Get the related CartItems
        cart_items = cart.items.all()

        if not cart_items.exists():
            return render(request, 'cart/cart_empty.html', {'error_message': "Your cart is empty."})

        # Safely load the services field for each cart item
        for item in cart_items:
            try:
                if isinstance(item.services, str):
                    item.services = json.loads(item.services)
            except (json.JSONDecodeError, TypeError) as e:
                item.services = []

        # Calculate the subtotal: sum of prices + service prices for all items
        subtotal = sum(item.total_price() for item in cart_items)

        # Retrieve delivery charge (this can come from the session or user input)
        # Example: Default to 0 or retrieve from user session
        delivery = Decimal(request.session.get('delivery', 0))

        # Calculate VAT (19%)
        vat = subtotal * Decimal('0.19')

        # Calculate grand total: subtotal + delivery charge + VAT
        grand_total = subtotal + delivery + vat
        grand_total = grand_total.quantize(Decimal('0.01'))

        # Prepare the context to pass to the template
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal.quantize(Decimal('0.01')),
            'delivery': delivery.quantize(Decimal('0.01')),
            'vat': vat.quantize(Decimal('0.01')),
            'grand_total': grand_total,
        }

        return render(request, 'cart/cart.html', context)

    except Cart.DoesNotExist:
        # Handle the case where the user doesn't have a cart yet
        return render(request, 'cart/cart_empty.html', {'error_message': "Your cart is empty."})

    except Exception as e:
        # Log any other errors and return a generic error page
        return render(request, 'cart/cart_error.html', {'error_message': "There was an error loading your cart."})

def add_to_cart(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        print(request.POST)
        print(request.FILES)

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        selected_size = request.POST.get('size')
        selected_services = request.POST.getlist('services')

        # Handle the case where size or quantity might be in a list format
        if isinstance(selected_size, list):
            selected_size = selected_size[0]

        selected_quantity_str = request.POST.get('quantity_option', '')

        # Validate that the quantity is a valid integer
        try:
            if selected_quantity_str:
                selected_quantity = int(selected_quantity_str)
            else:
                selected_quantity = 1
        except ValueError:
            messages.error(request, "Invalid quantity selected.")
            return redirect('cart:cart')

        selected_price = None
        for quantity in product.quantities:
            if quantity['quantity'] == selected_quantity:
                selected_price = Decimal(quantity['price'])
                break

        if selected_price is None:
            return redirect('cart:cart')

        servicePrices = {
            'Own Print Data Upload': Decimal('0.00'),
            'Online Designer': Decimal('35.00'),
            'Design Service': Decimal('40.00'),
            'Standard Production': Decimal('5.00'),
        }

        service_price = sum(
            servicePrices.get(
                service, Decimal('0.00')) for service in selected_services)

        # Check if the user is authenticated and get the cart
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            # Handle guest users (non-authenticated)
            cart_id = request.session.get('cart_id')
            if not cart_id:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
            else:
                cart = Cart.objects.get(id=cart_id)

        # Create the CartItem object
        cart_item = CartItem(
            cart=cart,
            product=product,
            size=selected_size,
            quantity=selected_quantity,
            price=selected_price,
            service_price=service_price,
            services=json.dumps(selected_services),
        )

        # Properly handle the services field here
        try:
            cart_item.services = json.loads(cart_item.services)
        except (json.JSONDecodeError, TypeError):
            cart_item.services = []

        cart_item.save()

        grand_total = sum(
            (item.price + item.service_price)
            for item in cart.items.all()
        )

        # Update the cart's total price
        cart.grand_total = grand_total.quantize(Decimal('0.01'))
        cart.save()

        # Save cart data to session
        request.session['cart_id'] = cart.id

        # Debugging output
        print(
            f"Added to cart: {product.name}, Size: {selected_size}, "
            f"Quantity: {selected_quantity}, Price: €{selected_price}, "
            f"Service Price: €{service_price}")
        print(f"Cart ID in session: {request.session.get('cart_id')}")

        messages.success(request, "Item added to your Cart!")

        return redirect('cart:cart')
    else:
        return redirect('cart:cart')


def remove_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        messages.info(request, 'Item removed from Cart.')
    except CartItem.DoesNotExist:
        pass

    return redirect('cart:cart')


def clear_cart(cart):
    """Clear the cart and reset its total."""
    cart.items.all().delete()
    cart.refresh_from_db()
    print(f"After delete: {cart.items.count()}")
    cart.grand_total = 0
    cart.save()


@csrf_exempt
@require_POST
def create_checkout_session(request):
    try:
        # Parse the JSON body manually
        data = json.loads(request.body)
        grand_total = data.get('grand_total')

        # Handle the case where 'grand_total' is not provided
        if not grand_total:
            return JsonResponse({'error': 'Missing grand_total'}, status=400)

        # Convert the grand total to the correct format for Stripe
        stripe_total = int(int(grand_total) * 100)

        order_number = uuid.uuid4().hex.upper()[:10]
        request.session['order_number'] = order_number

        # Create the Checkout Session
        success_url = f"{request.build_absolute_uri(
            reverse('cart:payment_success'))}?session_id={{CHECKOUT_SESSION_ID}}"
        print("Stripe success URL:", success_url)
        cancel_url = request.build_absolute_uri(
            reverse('cart:payment_cancel')
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f'Cart Total - Order #{order_number}',
                    },
                    'unit_amount': stripe_total,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )

        # Return the session ID to the frontend
        return JsonResponse({
            'sessionId': checkout_session.id,
            'orderNumber': order_number
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def payment_cancel(request):
    return render(request, 'checkout/cancel.html')


def payment_success(request):
    print("Payment success view started.")

    # Validate session
    session_id = validate_session(request)
    if not session_id:
        return redirect('cart:cart')

    try:
        # Retrieve session and payment intent
        session, intent = retrieve_session_and_intent(session_id)
        if not session or not intent:
            messages.error(request, "Error retrieving session or payment intent.")
            return redirect('cart:cart')

        # Check if payment was successful
        if not check_payment_success(intent):
            return redirect('cart:cart')

        # Retrieve order number
        order_number = request.session.get('order_number')
        if not order_number:
            messages.error(request, "No order number found.")
            print("No order number found.")
            return redirect('cart:cart')

        # Process the order and clear the cart
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            order = create_order(request)

            # Clear the cart
            clear_cart(cart)

            # Clear session data
            request.session.pop('cart_id', None)

            return render(request, 'cart/success.html', {
                'order_number': order_number,
                'amount': intent.amount / 100,
                'currency': intent.currency.upper(),
            })

        print("No cart found for the user.")
        return redirect('cart:cart')

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('cart:cart')


def validate_session(request):
    """Validate and retrieve session ID from request."""
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "No session ID provided.")
        print("No session ID provided.")
        return None
    return session_id


def retrieve_session_and_intent(session_id):
    """Retrieve Stripe session and payment intent."""
    try:
        print(f"Retrieving session for session_id: {session_id}")
        session = stripe.checkout.Session.retrieve(session_id)
        payment_intent_id = session.get('payment_intent')
        print(f"Retrieving payment intent for {payment_intent_id}")
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return session, intent
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None, None


def check_payment_success(intent):
    """Check if payment was successful."""
    if intent.status != 'succeeded':
        messages.error(request, "Payment was not successful.")
        print(f"Payment failed with status: {intent.status}")
        return False
    return True


def create_order_from_cart(user, cart, order_data):
    """Creates an order from the given cart and user"""
    if not cart or not cart.items.exists():
        raise ValueError("Cart is empty or missing.")

    order_total = Decimal(0)
    service_total = Decimal(0)
    delivery_total = Decimal(0)
    cart_total = Decimal(0)

    for item in cart.items.all():
        quantity_info = next(
            (q for q in item.product.quantities if q['quantity'] == item.quantity), None
        )
        item_price = Decimal(quantity_info['price']) if quantity_info else Decimal(0)
        cart_total += item_price
        service_total += Decimal(item.service_price)
        delivery_total += Decimal(item.delivery_price)

    grand_total = cart_total + service_total + delivery_total

    order = Order.objects.create(
        user=user,
        name=order_data.get('name', ''),
        email=order_data.get('email', ''),
        phone_number=order_data.get('phone_number', ''),
        country=order_data.get('country', ''),
        postcode=order_data.get('postcode', ''),
        town_or_city=order_data.get('town_or_city', ''),
        street_address1=order_data.get('street_address1', ''),
        street_address2=order_data.get('street_address2', ''),
        order_total=order_total,
        cart_total=cart_total,
        service_cost=service_total,
        delivery_cost=delivery_total,
        grand_total=grand_total
    )

    for item in cart.items.all():
        quantity_info = next(
            (q for q in item.product.quantities if q['quantity'] == item.quantity), None
        )
        item_price = Decimal(quantity_info['price']) if quantity_info else Decimal(0)
        OrderLineItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            lineitem_total=item_price,
            service_price=item.service_price,
            delivery_price=item.delivery_price
        )

    return order

def create_order(request):
    if not request.user.is_authenticated:
        return None

    cart = get_or_create_cart(request)

    # Get order data from POST
    order_data = {
        'name': request.POST.get('name', ''),
        'email': request.POST.get('email', ''),
        'phone_number': request.POST.get('phone_number', ''),
        'country': request.POST.get('country', ''),
        'postcode': request.POST.get('postcode', ''),
        'town_or_city': request.POST.get('town_or_city', ''),
        'street_address1': request.POST.get('street_address1', ''),
        'street_address2': request.POST.get('street_address2', ''),
    }

    order = create_order_from_cart(request.user, cart, order_data)

    # Clear cart after order is placed
    cart.items.all().delete()

    return order
