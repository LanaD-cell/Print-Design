from django.shortcuts import render, redirect
from cart.models import Cart
from django.http import Http404
from .models import Order, OrderLineItem
from .forms import CustomSignupForm
from decimal import Decimal
from django.contrib.auth import login
from .forms import OrderForm

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
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/order_checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51REARw07B3iAgZ7ifyoRqqH6yGr0rA2JrzjM4mgbnXVPXAezZDday4EXycdZzfHzwPOtjONqEyWlwJQpjab5RSHO00lcct7D8j',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
