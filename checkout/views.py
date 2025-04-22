from django.shortcuts import render, redirect
from cart.models import Cart
from cart.contexts import cart_contents
from django.http import Http404
from .models import Order, OrderLineItem
from .forms import CustomSignupForm
from decimal import Decimal
from django.contrib.auth import login
from .forms import OrderForm
from django.conf import settings
import stripe

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
        return render(request, 'registration/signup.html', {'signup_form': signup_form})

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

        # Find the price based on the selected quantity
        quantity_info = next((q for q in product.quantities if q['quantity'] == selected_quantity), None)
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
        quantity_info = next((q for q in product.quantities if q['quantity'] == selected_quantity), None)
        item_price = quantity_info['price'] if quantity_info else 0

        # Create order line item (now that the order has a primary key)
        OrderLineItem.objects.create(
            order=order,  # This is now valid since order has a primary key
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
    if request.method == 'POST':
        signup_form = CustomSignupForm(request.POST)
        if signup_form.is_valid():
            # Save the user and log them in
            user = signup_form.save()
            login(request, user)
            return redirect('create_cart_order')
    else:
        signup_form = CustomSignupForm()

    return render(request, 'registration/signup.html', {'form': signup_form})

def order_summary(request):
    return render(request, 'checkout/order_checkout.html')

def checkout(request):
    # Retrieve the cart using the cart_id stored in the session
    cart = Cart.objects.get(id=request.session.get('cart_id'))

    # If no cart is found, redirect to products page
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment.")
        return redirect('products')

    current_cart = cart_contents(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)

    # Define the delivery prices
    delivery_prices = {
        'Standard Production': Decimal('15.00'),
        '48h Express Production': Decimal('25.00'),
        '24h Express Production': Decimal('35.00')
    }

    # Get the selected delivery option from the POST request, defaulting to "Standard Production"
    delivery_option = request.POST.get('delivery_option', 'Standard Production')
    delivery_fee = delivery_prices.get(delivery_option, Decimal('5.00'))

    # Calculate the total price of the cart including the delivery fee
    cart_total = cart.total_price

    service_price = sum(item.service_price for item in cart.items.all())

    grand_total = cart_total + service_price + delivery_fee

    # Instantiate the order form and pass the required context to the template
    order_form = OrderForm()

    template = 'checkout/order_checkout.html'
    context = {
        'order_form': order_form,
        'cart': cart,
        'delivery_option': delivery_option,
        'delivery': delivery_fee,
        'service_price': service_price,
        'cart_total': cart_total,
        'grand_total': grand_total,
        'stripe_public_key': 'pk_test_51REARw07B3iAgZ7ifyoRqqH6yGr0rA2JrzjM4mgbnXVPXAezZDday4EXycdZzfHzwPOtjONqEyWlwJQpjab5RSHO00lcct7D8j',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
