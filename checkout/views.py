from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
import stripe
import json
from cart.models import Cart
from cart.contexts import cart_contents
from .models import OrderLineItem
from products.models import Product
from .models import Order, OrderLineItem
from homepage.models import Profile
from .forms import CustomSignupForm
from .forms import OrderForm
import logging
import re


def create_order(request):
    if not request.user.is_authenticated:
        # If the user is not logged in, show the signup form
        if request.method == 'POST':
            signup_form = CustomSignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                # Login the user after signing up
                login(request, user)
                # Redirect to the create_order view to process the order
                return redirect('create_cart_order')
        else:
            signup_form = CustomSignupForm()

        # Render the signup form
        return render(
            request, 'account/signup.html', {'signup_form': signup_form})

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist for this user.")

    cart_total = Decimal(0)
    total_service_price = Decimal(0)
    total_delivery_price = Decimal(0)

    # Loop through cart items
    for item in cart.items.all():
        product = item.product
        selected_quantity = item.quantity

        quantity_info = next(
            (
                q for q in product.quantities
                if q['quantity'] == selected_quantity
            ),
            None
        )
        if quantity_info:
            item_price = Decimal(quantity_info['price'])
        else:
            item_price = Decimal(0)

        cart_total += item_price
        total_service_price += Decimal(item.service_price)
        total_delivery_price += Decimal(item.delivery_price)

    # Now, create the order instance but don't save it yet
    order = Order(
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
        service_cost=total_service_price,
        delivery_cost=total_delivery_price,
        grand_total=cart_total + total_service_price + total_delivery_price
    )

    # Save the order to generate a primary key before proceeding
    order.save()

    # Now we can create the order line items
    for item in cart.items.all():
        product = item.product
        selected_quantity = item.quantity

        # Find the price based on the selected quantity
        quantity_info = next(
            (q for q in product.quantities if q['quantity'] == selected_quantity),
            None
        )
        item_price = quantity_info['price'] if quantity_info else 0

        # Create order line item
        OrderLineItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            lineitem_total=item_price,
            service_price=item.service_price,
            delivery_price=item.delivery_price
        )

    # Clear the cart items after creating the order
    cart.items.all().delete()

    grand_total = order.get_grand_total()

    return render(
        request, 'order/order_summary.html', {
            'order': order, 'grand_total': grand_total})


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


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            cart = Cart.objects.get(id=request.session.get('cart_id'))

            order = order_form.save()
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        # Retrieve the cart using the cart_id
        cart = Cart.objects.filter(id=request.session.get('cart_id')).first()

        if not cart:
            cart = Cart.objects.filter(user=request.user).first()

        # If no cart is found, redirect to products page
        if not cart or not cart.items.exists():
            messages.error(request, "There's nothing in your cart at the moment.")
            return redirect('homepage')

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        FREE_DELIVERY_THRESHOLD = Decimal(settings.FREE_DELIVERY_THRESHOLD)

        # Define the delivery prices
        delivery_prices = {
            'Standard Production': Decimal('15.00'),
            '48h Express Production': Decimal('25.00'),
            '24h Express Production': Decimal('35.00')
        }

        # Get the selected delivery option from the POST request
        delivery_option = request.POST.get('delivery_option', 'Standard Production')

        # Calculate the total price of the cart including the delivery fee
        cart_total = cart.total_price()
        service_price = sum(item.service_price for item in cart.items.all())

        delivery_fee = delivery_prices.get(delivery_option, Decimal('0.00'))

        if delivery_option == 'Standard Production':
            if cart_total >= FREE_DELIVERY_THRESHOLD:
                delivery_fee = Decimal('0.00')
            else:
                delivery_fee = Decimal('15.00')
        elif delivery_option == '48h Express Production':
            delivery_fee = Decimal('25.00')
        elif delivery_option == '24h Express Production':
            delivery_fee = Decimal('35.00')
        else:
            delivery_fee = Decimal('0.00')

        grand_total = cart_total + service_price + delivery_fee

        # Flag to check if the cart qualifies for free delivery
        free_delivery_qualified = cart_total >= FREE_DELIVERY_THRESHOLD

        user = request.user
        user_profile = getattr(user, 'profile', None)  # Safely get the profile

        # Set default values in case the profile fields are missing
        user_details = {
            'name': user.get_full_name(),
            'email': user.email,
            'phone_number': getattr(user_profile, 'phone_number', ''),
            'street_address1': getattr(user_profile, 'street_address1', ''),
            'town_or_city': getattr(user_profile, 'town_or_city', ''),
            'postcode': getattr(user_profile, 'postcode', ''),
            'country': getattr(user_profile, 'country', '')
        }

        order_form = OrderForm(initial=user_details)

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
                         Did you forget to add it to your environment?')

    template = 'checkout/order_checkout.html'
    context = {
        'order_form': order_form,
        'cart': cart,
        'delivery_option': delivery_option,
        'delivery': delivery_fee,
        'service_price': service_price,
        'cart_total': cart_total,
        'grand_total': grand_total,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'free_delivery_qualified': free_delivery_qualified,

        # Pass user details to be used in the hidden fields
        'hidden_name': user.get_full_name(),
        'hidden_email': user.email,
        'hidden_phone_number': getattr(user.profile, 'phone_number', ''),
        'hidden_country': getattr(user.profile, 'country', ''),
        'hidden_postcode': getattr(user.profile, 'postcode', ''),
        'hidden_town_or_city': getattr(user.profile, 'town_or_city', ''),
        'hidden_street_address1': getattr(user.profile, 'street_address1', ''),
        'hidden_street_address2': getattr(user.profile, 'street_address2', ''),
        'hidden_delivery_country': getattr(user.profile, 'delivery_country', ''),
        'hidden_delivery_postcode': getattr(user.profile, 'delivery_postcode', ''),
        'hidden_delivery_town_or_city': getattr(user.profile, 'delivery_town_or_city', ''),
        'hidden_delivery_street_address1': getattr(user.profile, 'delivery_street_address1', ''),
        'hidden_delivery_street_address2': getattr(user.profile, 'delivery_street_address2', ''),
    }

    return render(request, template, context)


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

