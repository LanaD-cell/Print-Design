import stripe
import os
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
import json
from cart.models import Cart, CartItem
from cart.contexts import cart_contents
from products.models import Product
from .models import Order, OrderLineItem
from homepage.models import Profile
from .forms import CustomSignupForm
from .forms import OrderForm
import logging
import re


stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

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


def create_order(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            signup_form = CustomSignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('create_cart_order')
        else:
            signup_form = CustomSignupForm()
        return render(request, 'account/signup.html', {'signup_form': signup_form})

    cart = get_or_create_cart(request)
    if not cart or not cart.items.exists():
        raise Http404("Cart is empty or missing.")

    cart_total = Decimal(0)
    service_total = Decimal(0)
    delivery_total = Decimal(0)

    for item in cart.items.all():
        quantity_info = next((q for q in item.product.quantities if q['quantity'] == item.quantity), None)
        item_price = Decimal(quantity_info['price']) if quantity_info else Decimal(0)
        cart_total += item_price
        service_total += Decimal(item.service_price)
        delivery_total += Decimal(item.delivery_price)

    order = Order.objects.create(
        user=request.user,
        name=request.POST.get('name', ''),
        email=request.POST.get('email', ''),
        phone_number=request.POST.get('phone_number', ''),
        country=request.POST.get('country', ''),
        postcode=request.POST.get('postcode', ''),
        town_or_city=request.POST.get('town_or_city', ''),
        street_address1=request.POST.get('street_address1', ''),
        street_address2=request.POST.get('street_address2', ''),
        order_total=cart_total,
        service_cost=service_total,
        delivery_cost=delivery_total,
        grand_total=cart_total + service_total + delivery_total
    )

    for item in cart.items.all():
        quantity_info = next((q for q in item.product.quantities if q['quantity'] == item.quantity), None)
        item_price = quantity_info['price'] if quantity_info else 0
        OrderLineItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            lineitem_total=item_price,
            service_price=item.service_price,
            delivery_price=item.delivery_price
        )

    cart.items.all().delete()
    grand_total = order.get_grand_total()

    return render(request, 'order/order_summary.html', {
        'order': order, 'grand_total': grand_total
    })


def signup_view(request):
    confirm_password_success = None

    if request.method == 'POST':
        signup_form = CustomSignupForm(request.POST)
        if signup_form.is_valid():
            password1 = signup_form.cleaned_data.get('password1')
            password2 = signup_form.cleaned_data.get('password2')

            if password1 == password2:
                confirm_password_success = "Passwords match!"

            # Save the user and log them in
            user = signup_form.save()
            login(request, user)

            # Create the user's profile after signup
            Profile.objects.create(
                user=user,
                phone_number='',
                country='',
                postcode='',
                town_or_city='',
                street_address1='',
                street_address2='',
            )

            return redirect('create_cart_order')
    else:
        signup_form = CustomSignupForm()

    return render(request, 'account/signup.html', {
        'form': signup_form,
        'confirm_password_success': confirm_password_success
    })


def order_summary(request):
    return render(request, 'checkout/order_checkout.html')


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        selected_size = request.POST.get('size')
        selected_services = request.POST.getlist('services')

        selected_quantity = request.POST.get('quantity_option', '1')
        try:
            selected_quantity = int(selected_quantity)
        except ValueError:
            messages.error(request, "Invalid quantity.")
            return redirect('cart:cart_details')

        selected_price = next(
            (Decimal(q['price']) for q in product.quantities if q['quantity'] == selected_quantity),
            None
        )
        if selected_price is None:
            messages.error(request, "Selected quantity not available.")
            return redirect('cart:cart_details')

        service_prices = {
            'Own Print Data Upload': Decimal('0.00'),
            'Online Designer': Decimal('35.00'),
            'Design Service': Decimal('40.00'),
            'Standard Production': Decimal('0.00'),
            'Priority Production': Decimal('15.00'),
            '48h Express Production': Decimal('25.00'),
            '24h Express Production': Decimal('35.00'),
        }
        service_price = sum(service_prices.get(s, Decimal('0.00')) for s in selected_services)

        file = request.FILES.get('print_data_file')
        if 'Own Print Data Upload' in selected_services and file:
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to upload files.")
                return redirect('login')

            print_data = PrintData.objects.create(
                user=request.user,
                product=product,
                uploaded_file=file,
                service_type='Own Print Data Upload'
            )
            request.user.profile.print_data_files.add(print_data)
            request.user.profile.save()

        cart = get_or_create_cart(request)

        CartItem.objects.create(
            cart=cart,
            product=product,
            size=selected_size,
            quantity=selected_quantity,
            price=selected_price,
            service_price=service_price,
            services=json.dumps(selected_services),
        )

        cart.total_price = cart.total_price()
        cart.save()
        request.session['cart_id'] = cart.id

        messages.success(request, "Item added to your Cart!")
        return redirect('cart:cart_details')

    return redirect('cart:cart_details')


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.error(request, "There's nothing in your cart.")
        return redirect('homepage')

    current_cart = cart_contents(request)
    cart_total = current_cart['cart_total']
    service_price = current_cart['service_price']

    delivery_option = request.POST.get('delivery_option', 'Standard Production')
    delivery_prices = {
        'Standard Production': Decimal('15.00'),
        '48h Express Production': Decimal('25.00'),
        '24h Express Production': Decimal('35.00'),
    }

    delivery_fee = delivery_prices.get(delivery_option, Decimal('0.00'))
    if delivery_option == 'Standard Production' and cart_total >= Decimal(settings.FREE_DELIVERY_THRESHOLD):
        delivery_fee = Decimal('0.00')

    grand_total = cart_total + service_price + delivery_fee
    stripe_total = int(grand_total * 100)

    payment_intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency='eur',
    )
    user = request.user
    profile = getattr(user, 'profile', None)
    initial_data = {
        'name': user.get_name(),
        'email': user.email,
        'phone_number': getattr(profile, 'phone_number', ''),
        'street_address1': getattr(profile, 'street_address1', ''),
        'town_or_city': getattr(profile, 'town_or_city', ''),
        'postcode': getattr(profile, 'postcode', ''),
        'country': getattr(profile, 'country', '')
    }

    order_form = OrderForm(initial=initial_data)

    context = {
        'order_form': order_form,
        'cart': cart,
        'delivery_option': delivery_option,
        'delivery': delivery_fee,
        'service_price': service_price,
        'cart_total': cart_total,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': payment_intent.client_secret,
        'free_delivery_qualified': cart_total >= Decimal(settings.FREE_DELIVERY_THRESHOLD),
    }

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')

    return render(request, 'checkout/order_checkout.html', context)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Get cart contents from session
            cart = cart_contents(request)
            grand_total = int(cart['grand_total'] * 100)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Order from YourSite',
                        },
                        'unit_amount': grand_total,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/checkout/checkout_success_page/{CHECKOUT_SESSION_ID}/'),
                cancel_url=request.build_absolute_uri('/checkout/summary/'),
            )
            return JsonResponse({'sessionId': session.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def checkout_success(request, order_number):
    """
    Handle successful checkout
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def create_payment_intent(request):
    try:
        # Parse the JSON body of the request
        data = json.loads(request.body)

        # Get the grand_total (in currency) and id_name from the received data
        grand_total = data.get('grand_total')
        id_name = data.get('id_name')

        # Ensure that grand_total and id_name are provided
        if not grand_total or not id_name:
            return JsonResponse({'error': 'Missing grand_total or id_name'}, status=400)

        # Convert grand_total to cents (Stripe expects amounts in cents)
        amount_in_cents = int(grand_total * 100)

        # Create the PaymentIntent with the amount and metadata
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency='eur',
            metadata={'id_name': id_name}
        )

        # Return the client secret to the frontend
        return JsonResponse({'clientSecret': payment_intent['client_secret']})

    except Exception as e:
        # Return an error if any exception occurs
        return JsonResponse({'error': str(e)}, status=400)

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
def payment_success(request, order_number):
    session_id = request.GET.get('session_id')

    # If no session_id is present, redirect to order summary page
    if not session_id:
        return redirect('checkout:order_summary')

    try:
        # Retrieve the Stripe session using the session_id
        session = stripe.checkout.Session.retrieve(session_id)

        # Extract necessary details from the Stripe session
        customer_email = session.customer_details.email
        amount_total = session.amount_total / 100

        # Fetch the associated order
        order = get_object_or_404(Order, order_number=order_number)

        # Check if the session ID corresponds to the order number
        if order.order_number != session.id:
            raise Http404("Order not found for this session.")

        # If payment was successful, update the order status
        if session.payment_status == 'paid':
            order.status = 'Paid'
            order.save()

            # Optionally save some information to the user profile or any other place if needed
            # Profile related actions, etc.

            # Clear the cart from session after successful payment
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True

            # Display the success page with order details
            return render(request, 'checkout/success.html', {'order': order})

        else:
            # If payment was not successful, handle accordingly
            return render(request, 'checkout/payment_failed.html')

    except stripe.error.StripeError as e:
        # Handle Stripe API errors
        logger.error(f"Stripe error: {e.user_message}")

        return redirect('checkout:checkout_success_page', order_number=order_number)

    except Exception as e:
        # Handle other exceptions
        logger.error(f"Error during payment success processing: {str(e)}")
        return redirect('checkout:order_summary')
