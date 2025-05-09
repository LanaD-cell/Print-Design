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
from decimal import Decimal, ROUND_HALF_UP
import json
import threading  # For background task

stripe.api_key = settings.STRIPE_SECRET_KEY


def view_cart(request):
    try:
        # Get the user's cart, raise an exception if not found
        cart = Cart.objects.get(user=request.user)
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

        subtotal = sum(item.total_price() for item in cart_items)

        delivery = Decimal(request.session.get('delivery', 0))

        # Calculate VAT (19%)
        vat = subtotal * Decimal('0.19')

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

        # Get personal and delivery details
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        address_line_1 = data.get('address_line_1')
        town_or_city = data.get('town_or_city')
        postcode = data.get('postcode')
        country = data.get('country')

        grand_total = data.get('grand_total')

        # Handle the case where 'grand_total' is not provided
        if not grand_total:
            return JsonResponse({'error': 'Missing grand_total'}, status=400)

        grand_total_decimal = Decimal(str(grand_total))
        delivery_fee = Decimal('5.00')
        final_total = grand_total_decimal + delivery_fee
        stripe_total = int((final_total * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

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
            metadata={
                'name': name,
                'email': email,
                'phone': phone,
                'address_line_1': address_line_1,
                'town_or_city': town_or_city,
                'postcode': postcode,
                'country': country,
                'order_number': order_number,
            }
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


def process_cart_and_order(cart, order_number):
    try:
        print(f"Processing cart for order {order_number}...")
        # Extract user and cart data
        user = cart.user
        order_number = order_number
        name = user.get_full_name() if user.get_full_name() else user.username
        email = user.email

        # Additional fields from user profile (if they exist)
        phone_number = user.profile.phone_number if hasattr(user, 'profile') else ''
        country = user.profile.country if hasattr(user, 'profile') else ''
        postcode = user.profile.postcode if hasattr(user, 'profile') else ''
        town_or_city = user.profile.town_or_city if hasattr(user, 'profile') else ''
        street_address1 = user.profile.street_address1 if hasattr(user, 'profile') else ''

        # Calculate the cart totals (including VAT and delivery)
        cart_total = Decimal(cart.items_subtotal())
        vat = Decimal(cart.calculate_vat(cart_total))
        delivery_cost = Decimal(cart.get_delivery_price())
        grand_total = cart_total + vat + delivery_cost

        # Create the order
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            name=name,
            email=email,
            phone_number=phone_number,
            country=country,
            postcode=postcode,
            town_or_city=town_or_city,
            street_address1=street_address1,
            order_total=cart_total,
            cart_total=cart_total,
            grand_total=grand_total,
            service_cost=0.00,
            delivery_cost=delivery_cost,
            status=Order.PAID
        )

        # Create OrderLineItems for each CartItem
        for cart_item in cart.items.all():
            OrderLineItem.objects.create(
                order=order,
                product=cart_item.product,
                product_size=cart_item.size,
                quantity=cart_item.quantity,
                lineitem_total=Decimal(cart_item.total_price()),
                service_price=Decimal(cart_item.service_price),
                additional_services=cart_item.services
            )

        cart.items.all().delete()
        print(f"Cart cleared. Remaining items: {cart.items.count()}")

        print(f"Order created successfully for {order_number}")

    except Exception as e:
        print(f"Error while processing cart: {str(e)}")

def payment_success(request):
    print("Payment success view started.")

    # Validate session ID in URL
    session_id = validate_session(request)
    if not session_id:
        print("Session validation failed.")
        messages.error(request, "Missing session ID.")
        return redirect('cart:cart')

    try:
        # Get session and intent from Stripe
        session, intent = retrieve_session_and_intent(session_id)
        print(f"Stripe session: {session}")
        print(f"Stripe intent: {intent}")

        if not session or not intent:
            print("Session or intent retrieval failed.")
            messages.error(request, "Stripe payment confirmation failed.")
            return redirect('cart:cart')

        # Ensure payment was actually successful
        if not check_payment_success(intent):
            print("Stripe reported payment failure.")
            messages.error(request, "Payment was not successful.")
            return redirect('cart:cart')

        # Optional order number (not required for success display)
        order_number = request.session.get('order_number', 'UNKNOWN')
        print(f"Order number: {order_number}")

        if "cart" in request.session:
            print("Cart in session:", request.session["cart"])

            del request.session["cart"]
            request.session.modified = True
            request.session.save()
            print("Cart deleted from session")
        else:
            print("No cart found in session")

        # Prepare success page response
        response = render(request, 'cart/success.html', {
            'order_number': order_number,
            'amount': intent.amount / 100,
            'currency': intent.currency.upper(),
        })

        # Optional: create order in background
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            threading.Thread(
                target=process_cart_and_order,
                args=(cart, order_number)
            ).start()

        return response

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        messages.error(request, "An unexpected error occurred.")
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
        order_total=order_total,
        cart_total=cart_total,
        service_cost=service_total,
        delivery_cost=delivery_total,
        grand_total=grand_total,
        session_id=order_data.get('session_id', '')
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
    }

    order = create_order_from_cart(request.user, cart, order_data)

    # Clear cart after order is placed
    cart.items.all().delete()

    return order

@login_required
def order_detail(request, order_number):
    print(f"Requested order number: {order_number}")
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_line_items = order.line_items.all()
    return render(request, 'cart/order_detail.html', {
        'order': order,
        'order_number': order.order_number,
        'amount': order.grand_total,
        'order_line_items': order_line_items,
        'user': request.user,
    })
