import stripe
from dotenv import load_dotenv
import os
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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


load_dotenv()

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


def create_checkout_session(request):
    try:
        # Retrieve the current order from session
        order_id = request.session.get('order_id')
        if not order_id:
            return JsonResponse({'error': 'No order found in session'}, status=400)

        order = Order.objects.get(id=order_id)
        cart = Cart.objects.get(id=request.session.get('cart_id'))  # Assuming cart is stored in session

        # Convert to cents (Stripe expects amounts in cents)
        stripe_total = int(order.grand_total * 100)

        # Create an empty list for line items
        line_items = []

        # Iterate over cart items and add each product's info as a line item
        for item in cart.items.all():
            product = item.product
            size = item.product_size
            quantity = item.quantity
            price = item.price

            # Add size and quantity to the product name for Stripe
            product_name = f"{product.name} ({size})" if size else product.name

            # Calculate the price for the quantity selected
            product_price = price * quantity

            line_items.append({
                'price_data': {
                    'currency': settings.STRIPE_CURRENCY,
                    'product_data': {
                        'name': product_name,
                    },
                    'unit_amount': int(product_price * 100),
                },
                'quantity': quantity,
            })

        # Create a Stripe Checkout session with multiple line items
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',  # One-time payment mode
            success_url=request.build_absolute_uri('/checkout/success/'),  # URL for successful payment
            cancel_url=request.build_absolute_uri('/checkout/cancel/'),  # URL for canceled payment
        )

        # Redirect the user to the Stripe Checkout page
        return redirect(session.url, code=303)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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

    order_amount = grand_total

    grand_total = cart_total + service_price + delivery_fee
    payment_intent = stripe.PaymentIntent.create(
        amount=order_amount,
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

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)

logger = logging.getLogger(__name__)


@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            full_name = data.get('full_name')

            # Create the payment intent with a test amount of $20 (2000 cents)
            intent = stripe.PaymentIntent.create(
                amount=2000,  # amount in cents
                currency='eur',
                description=f"Payment for {full_name}",
            )

            # Return the client secret
            return JsonResponse({'clientSecret': intent.client_secret})

        except Exception as e:
            # Return an error message in case of failure
            return JsonResponse({'error': str(e)}, status=500)

    # If the method isn't POST, return an error
    return JsonResponse({'error': 'Invalid request method'}, status=400)


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


def payment_success(request):
    order_number = request.GET.get('order_number')  # You may pass order_number in the URL params or session
    if order_number:
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            raise Http404("Order not found")

        return render(request, 'checkout/success.html', {'order': order})
    else:
        # If no order_number is provided in the query params, handle the case (e.g., show a generic success message)
        return render(request, 'checkout/success.html', {'message': 'Your payment was successful!'})