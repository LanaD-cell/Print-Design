from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Cart, CartItem
from django.conf import settings
import uuid
import stripe
from .models import Cart
from homepage.models import PrintData
from django.contrib import messages
from decimal import Decimal
import json
import logging


# Initialize logger
logger = logging.getLogger(__name__)

@login_required
def view_cart(request):
    try:
        logger.info(f"User {request.user} is accessing their cart.")

        # Get the user's cart, raise an exception if not found
        cart = Cart.objects.get(user=request.user)
        logger.info(f"Cart found for user {request.user}: {cart.id}")

        # Get the related CartItems
        cart_items = cart.items.all()
        logger.info(f"Found {len(cart_items)} items in the cart.")

        # Safely load the services field for each cart item
        for item in cart_items:
            try:
                if isinstance(item.services, str):
                    item.services = json.loads(item.services)
                logger.info(f"Services for item {item.id}: {item.services}")
            except (json.JSONDecodeError, TypeError) as e:
                item.services = []
                logger.warning(f"Failed to decode services for item {item.id}: {e}")

        # Calculate the subtotal: sum of prices + service prices for all items
        subtotal = sum(item.total_price() for item in cart_items)
        logger.info(f"Subtotal calculated: {subtotal} EUR.")

        # Retrieve delivery charge (this can come from the session or user input)
        # Example: Default to 0 or retrieve from user session
        delivery = Decimal(request.session.get('delivery', 0))  # Default delivery charge to 0 if not set
        logger.info(f"Delivery charge: {delivery} EUR.")

        # Calculate VAT (19%)
        vat = subtotal * Decimal('0.19')
        logger.info(f"VAT (19%) calculated: {vat} EUR.")

        # Calculate grand total: subtotal + delivery charge + VAT
        grand_total = subtotal + delivery + vat
        grand_total = grand_total.quantize(Decimal('0.01'))  # Round to 2 decimal places
        logger.info(f"Grand total calculated: {grand_total} EUR.")

        # Prepare the context to pass to the template
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal.quantize(Decimal('0.01')),  # Ensure 2 decimal places
            'delivery': delivery.quantize(Decimal('0.01')),  # Ensure 2 decimal places
            'vat': vat.quantize(Decimal('0.01')),  # Ensure 2 decimal places
            'grand_total': grand_total,
        }

        return render(request, 'cart/cart.html', context)

    except Cart.DoesNotExist:
        # Handle the case where the user doesn't have a cart yet
        logger.warning(f"User {request.user} does not have a cart.")
        return render(request, 'cart/cart_empty.html', {'error_message': "Your cart is empty."})

    except Exception as e:
        # Log any other errors and return a generic error page
        logger.error(f"Error loading cart for user {request.user}: {str(e)}")
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
            'Standard Production': Decimal('0.00'),
            'Priority Production': Decimal('15.00'),
            '48h Express Production': Decimal('25.00'),
            '24h Express Production': Decimal('35.00'),
        }

        # Debugging purpose
        print(request.POST)

        # Map the selected services to their corresponding price values
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


stripe.api_key = settings.STRIPE_SECRET_KEY

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
        stripe_total = int(float(grand_total) * 100)

        order_number = uuid.uuid4().hex.upper()[:10]
        request.session['order_number'] = order_number

        # Create the Checkout Session
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
            success_url=request.build_absolute_uri('checkout/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )

        request.session['order_number'] = order_number

        # Return the session ID to the frontend
        return JsonResponse({
            'sessionId': checkout_session.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def payment_cancel(request):
    return render(request, 'checkout/cancel.html')


def checkout_success_page(request, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        order_id = session.client_reference_id
        order = get_object_or_404(Order, id=order_id)
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e.user_message}")
        messages.error(request, "An error occurred while processing the payment.")
        return redirect('checkout:summary')
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        messages.error(request, "An unexpected error occurred.")
        return redirect('checkout:summary')

    return render(request, 'checkout/success.html', {'order': order})


@csrf_exempt
def payment_confirm(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            payment_method = data.get('payment_method')
            client_secret = data.get('client_secret')

            # Log the data to ensure client_secret is passed correctly
            logger.debug(f"Received payment_method: {payment_method}, client_secret: {client_secret}")

            # Extract the PaymentIntent ID from the client_secret
            match = re.match(r'^(pi_[^_]+)', client_secret or '')
            if not match:
                return JsonResponse({'success': False, 'error': 'Invalid client secret'})

            payment_intent_id = match.group(1)

            intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method=payment_method
            )

            if intent.status == 'succeeded':
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Payment failed'})

        except stripe.error.StripeError as e:
            return JsonResponse({'success': False, 'error': str(e)})

        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def payment_success(request):
    # Get session_id from URL
    session_id = request.GET.get('session_id')

    if session_id:
        try:
            # Retrieve the session using the session_id
            session = stripe.checkout.Session.retrieve(session_id)

            # Retrieve the associated payment_intent
            payment_intent_id = session.get('payment_intent')

            if payment_intent_id:
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)

                if intent.status == 'succeeded':
                    # Process order logic here
                    return render(request, 'checkout/success.html', {'order_number': intent.id})
                else:
                    messages.error(request, "Payment was not successful.")
            else:
                messages.error(request, "No payment intent found.")

        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('checkout:summary')