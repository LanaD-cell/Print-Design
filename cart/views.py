from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Cart, CartItem
from django.conf import settings
import stripe
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

        # Process each cart item and handle services
        for item in cart_items:
            try:
                # Attempt to decode the JSON string stored in 'services'
                item.services = json.loads(item.services)
                logger.info(f"Services for item {item.id}: {item.services}")
            except (json.JSONDecodeError, TypeError):
                item.services = []  # Set to an empty list if decoding fails
                logger.warning(f"Failed to decode services for item {item.id}, setting to empty list.")

        # Use the method from the Cart model to calculate the total price
        total_price = cart.total_price()
        logger.info(f"Total price for the cart: {total_price} EUR.")

        # Prepare the context to pass to the template
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
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

        # Handle the 'Own Print Data Upload' service, if selected
        file = None
        if 'Own Print Data Upload' in selected_services and \
                'print_data_file' in request.FILES:
            file = request.FILES['print_data_file']

        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Show an error message
            messages.error(
                request, "Please sign up or log in to upload print data.")

            # Redirect to the login page
            return redirect('login')

        # Create a PrintData object and link it to the user, only if a file was uploaded
        if file:
            print_data = PrintData.objects.create(
                user=request.user,
                product=product,
                uploaded_file=file,
                service_type='Own Print Data Upload'
            )

            request.user.profile.print_data_files.add(print_data)
            request.user.profile.save()

            messages.success(request, f"Print data uploaded: {file.name} for product {product.name}")

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

        # Update the cart's total price
        cart.total_price = cart.total_price()
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

        return redirect('cart:cart_details')
    else:
        return redirect('cart:cart_details')


def remove_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        messages.info(request, 'Item removed from Cart.')
    except CartItem.DoesNotExist:
        pass

    return redirect('cart:cart_details')


stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt  # Ensure CSRF token doesn't block the request
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            success_url = request.build_absolute_uri(
                reverse('checkout:checkout_success_page', args=['{CHECKOUT_SESSION_ID}']))

            # Create a new Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': 'Total',
                            },
                            'unit_amount': int(data['grand_total'] * 100),
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=success_url,
                cancel_url=request.build_absolute_uri(
                    reverse('cart:payment_cancel')),
                )

            # Return the session ID to the frontend
            return JsonResponse({
                'sessionId': session.id
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        grand_total = data.get('grand_total')
        if not grand_total:
            return JsonResponse({'error': 'Missing grand_total'}, status=400)

        stripe_total = int(float(grand_total) * 100)

        payment_intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency='eur',
            automatic_payment_methods={'enabled': True},
        )

        return JsonResponse({'client_secret': payment_intent.client_secret})
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

    return render(request, 'checkout/order_summary.html', {'order': order})


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
    client_secret = request.GET.get('payment_intent_client_secret')
    try:
        intent = stripe.PaymentIntent.retrieve(request.GET.get('payment_intent'))
        if intent.status == 'succeeded':
            # Process order logic here
            ...
            return render(request, 'checkout/success.html')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('checkout:summary')
