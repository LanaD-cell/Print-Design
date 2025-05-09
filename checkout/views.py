import stripe
import os
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
from .utils import get_or_create_cart
from .models import Order, OrderLineItem
from homepage.models import Profile
from .forms import CustomSignupForm
from .forms import OrderForm
from .utils import get_or_create_cart
import re

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_cart_total(request):
    # Get the cart for the current user,
    # or use a mock cart object for testing
    cart = get_or_create_cart(request)

    # Let's assume these methods are available on the cart object
    cart_total = cart.grand_price()
    delivery_fee = cart.delivery_fee() if cart.items.exists() else Decimal('0.00')
    vat_amount = cart.vat_amount()
    grand_total = cart_total + delivery_fee + vat_amount

    # Return the data as JSON
    return JsonResponse({
        'cart_total': str(cart_total),
        'delivery_fee': str(delivery_fee),
        'vat_amount': str(vat_amount),
        'grand_total': str(grand_total)
    })


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.error(request, "There's nothing in your cart.")
        return redirect('homepage')

    current_cart = cart_contents(request)
    cart_total = cart.grand_price()
    service_price = Decimal(0)

    delivery_option = request.POST.get(
        'delivery_option', 'Standard Production')
    delivery_prices = {
        'Standard Production': Decimal('5.00'),
    }

    delivery_fee = delivery_prices.get(delivery_option, Decimal('0.00')) if cart.items.exists() else Decimal('0.00')

    grand_total = cart_total + service_price + delivery_fee
    stripe_total = int(grand_total * 100)

    payment_intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency='eur',
    )
    user = request.user
    profile = getattr(user, 'profile', None)
    initial_data = {
        'name': user.get_full_name() or user.username,
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
    }

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')

    return render(request, 'cart:cart.html', context)


def create_order(request, cart):
    # If the user is not authenticated, redirect them to the signup page.
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

    # Ensure the cart exists and has items.
    cart = get_or_create_cart(request)
    if not cart or not cart.items.exists():
        raise Http404("Cart is empty or missing.")

    # Initialize totals for the order.
    order_total = Decimal(0)
    service_total = Decimal(0)
    delivery_total = Decimal(0)
    cart_total = Decimal(0)

    # Create the order object first
    order = Order.objects.create(
        user=request.user,
        name=request.POST.get('name', ''),
        email=request.POST.get('email', ''),
        phone_number=request.POST.get('phone_number', ''),
        country=request.POST.get('country', ''),
        postcode=request.POST.get('postcode', ''),
        town_or_city=request.POST.get('town_or_city', ''),
        street_address1=request.POST.get('street_address1', ''),
    )

    # Now loop through cart items and create OrderLineItems.
    for item in cart.items.all():
        quantity_info = next(
            (q for q in item.product.quantities if q['quantity'] == item.quantity),
            None
        )

        item_price = Decimal(quantity_info['price']) if quantity_info else Decimal(0)
        order_total += item_price
        cart_total += item_price
        service_total += Decimal(item.service_price)
        delivery_total += Decimal(item.delivery_price)

        # Create the order line item for each cart item.
        OrderLineItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            lineitem_total=item_price,
            service_price=item.service_price,
            delivery_price=item.delivery_price
        )

    # Update the order with the calculated totals.
    order.order_total = order_total
    order.cart_total = cart_total
    order.service_cost = service_total
    order.delivery_cost = delivery_total
    order.grand_total = cart_total + service_total + delivery_total
    order.save()

    if 'cart' in request.session:
        del request.session['cart']

    return order


@csrf_exempt
def payment_confirm(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            payment_method = data.get('payment_method')
            client_secret = data.get('client_secret')

            # Extract the PaymentIntent ID from the client_secret
            match = re.match(r'^(pi_[^_]+)', client_secret or '')
            if not match:
                return JsonResponse(
                    {'success': False, 'error': 'Invalid client secret'})

            payment_intent_id = match.group(1)

            intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method=payment_method
            )

            if intent.status == 'succeeded':
                return JsonResponse({'success': True})
            else:
                return JsonResponse(
                    {'success': False, 'error': 'Payment failed'})

        except stripe.error.StripeError as e:
            return JsonResponse({'success': False, 'error': str(e)})

        except Exception as e:
            return JsonResponse(
                {'success': False, 'error': 'An error occurred: ' + str(e)})

    return JsonResponse(
        {'success': False, 'error': 'Invalid request method'})


def signup_view(request):
    confirm_password_success = None

    if request.method == 'POST':
        signup_form = CustomSignupForm(request.POST)
        if signup_form.is_valid():
            password1 = signup_form.cleaned_data.get('password1')
            password2 = signup_form.cleaned_data.get('password2')

            if password1 == password2:
                confirm_password_success = "Passwords match!"

            user = signup_form.save()
            login(request, user)

            Profile.objects.create(
                user=user,
                phone_number='',
                country='',
                postcode='',
                town_or_city='',
                street_address1='',
            )

            return redirect('create_cart_order')
    else:
        signup_form = CustomSignupForm()

    return render(request, 'account/signup.html', {
        'form': signup_form,
        'confirm_password_success': confirm_password_success
    })


def order_summary(request):
    return render(request, 'cart:success.html')


def checkout_success_page(request, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        order_id = session.client_reference_id
        order = get_object_or_404(Order, id=order_id)
    except stripe.error.StripeError as e:
        messages.error(request, "An error occurred while processing the payment.")
        return redirect('cart:cart')
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        return redirect('cart:cart')

    context = {
        'order': order,
        'order_number': order.id,
        'amount': order.grand_total,
    }

    return render(request, 'cart/success.html', context)

def create_payment_intent(request):
    try:
        # Assuming 'grand_total' comes from the request body
        data = json.loads(request.body)
        grand_total = data.get('grand_total')

        # Check if grand_total is provided
        if not grand_total:
            return JsonResponse({'error': 'Missing grand_total'}, status=400)

        # Convert the grand total into the smallest currency unit (cents)
        stripe_total = int(grand_total * 100)

        # Create the PaymentIntent with the calculated total
        payment_intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency='eur',
        )

        # Return the client_secret to confirm the payment on the frontend
        return JsonResponse({'client_secret': payment_intent.client_secret})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
