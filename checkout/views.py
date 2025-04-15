from django.shortcuts import render, redirect
from cart.models import Cart
from django.http import Http404
from .models import Order, OrderLineItem


def create_order(request):
    if not request.user.is_authenticated:
        # If the user is not logged in, show the signup form
        if request.method == 'POST':
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                # Login the user after signing up
                login(request, user)
                # Redirect to the create_order view to process the order
                return redirect('create_order')
        else:
            signup_form = UserCreationForm()

        # Render the signup form
        return render(request, 'account/signup.html', {'signup_form': signup_form})

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist for this user.")

    cart_total = 0
    total_service_price = 0
    total_delivery_price = 0

    # Loop through cart items
    for item in cart.items.all():
        product = item.product
        selected_quantity = item.quantity

        # Find the price based on the selected quantity
        quantity_info = next((q for q in product.quantities if q['quantity'] == selected_quantity), None)
        if quantity_info:
            item_price = quantity_info['price']
        else:
            item_price = 0

        cart_total += item_price

        # Calculate additional services price
        total_service_price += item.service_price

        # Calculate delivery price
        total_delivery_price += item.delivery_price

    # Now, create the order
    order = Order.objects.create(
        user=request.user,
        full_name=request.POST['full_name'],
        email=request.POST['email'],
        phone_number=request.POST['phone_number'],
        country=request.POST['country'],
        postcode=request.POST.get('postcode', ''),
        town_or_city=request.POST['town_or_city'],
        street_address1=request.POST['street_address1'],
        street_address2=request.POST.get('street_address2', ''),
        order_total=cart_total,
        service_cost=total_service_price,
        delivery_cost=total_delivery_price,
        grand_total=cart_total + total_service_price + total_delivery_price
    )

    order.save()

    # Create order items for each item in the cart
    for item in cart.items.all():
        product = item.product
        selected_quantity = item.quantity

        # Find the price based on the selected quantity
        quantity_info = next((q for q in product.quantities if q['quantity'] == selected_quantity), None)
        item_price = quantity_info['price'] if quantity_info else 0

        # Create order item
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
