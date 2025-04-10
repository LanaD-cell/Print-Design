from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Order
from decimal import Decimal


def view_cart(request):
    # Get the selected summary data from the session
    selected_size = request.session.get('selected_size', 'None')
    selected_quantity = request.session.get('selected_quantity', 'None')
    selected_services = request.session.get('selected_services', [])
    selected_delivery = request.session.get('selected_delivery', 'None')
    total_price = request.session.get('total_price', 0)

    # Pass the data to the cart.html template
    context = {
        'selected_size': selected_size,
        'selected_quantity': selected_quantity,
        'selected_services': selected_services,
        'selected_delivery': selected_delivery,
        'total_price': total_price,
    }

    return render(request, 'cart/cart.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        print("POST data:", request.POST)

        # Get the product ID from the POST data
        product_id = request.POST.get('product_id')
        # Retrieve the product from the database
        product = get_object_or_404(Product, id=product_id)

        # Get selected values from the form
        selected_size = request.POST.get('size')
        selected_quantity = int(request.POST.get('quantity_option')[0])
        selected_services = request.POST.getlist('services')
        selected_delivery = request.POST.get('delivery_options')

        # Ensure only one size and quantity are selected
        if isinstance(selected_size, list):
            selected_size = selected_size[0]

        if isinstance(selected_quantity, list):
            selected_quantity = selected_quantity[0]

        # Fetch the corresponding price based on the selected quantity for the product
        selected_price = None
        for quantity in product.quantities:
            if quantity['quantity'] == selected_quantity:
                selected_price = Decimal(quantity['price'])
                break

        if selected_price is None:
            # If no price was found for the selected quantity, handle the error
            return redirect('cart:cart')

        # Define service prices
        servicePrices = {
            'own_print_data_option': Decimal('0.00'),
            'online_designs': Decimal('35.00'),
            'design_services': Decimal('40.00')
        }

        # Define delivery prices
        deliveryPrices = {
            'Standard Production': Decimal('5.00'),
            '48h Express Production': Decimal('10.00'),
            '24h Express Production': Decimal('15.00')
        }

        # Calculate service price
        service_price = Decimal('0.00')
        for service in selected_services:
            service_price += servicePrices.get(service, Decimal('0.00'))

        # Get the delivery price
        delivery_price = deliveryPrices.get(selected_delivery, Decimal('0.00'))

        # Create or get the cart for the user (assuming user is logged in)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Total item price
        total_item_price = selected_price + service_price + delivery_price

        # Create a new CartItem instance with the selected details
        cart_item = CartItem(
            cart=cart,
            product=product,
            size=selected_size,
            quantity=selected_quantity,
            price=selected_price,
            service_price=service_price,
            delivery_price=delivery_price,
            total_price=total_item_price
        )

        # Save the CartItem
        cart_item.save()

        # Update cart total price
        cart.total_price += total_item_price
        cart.save()

        # Save cart data to session (for view_cart)
        request.session['selected_size'] = selected_size
        request.session['selected_quantity'] = selected_quantity
        request.session['selected_services'] = selected_services
        request.session['selected_delivery'] = selected_delivery
        request.session['total_price'] = cart.total_price

        # Print for debugging
        print(f"Added to cart: Product {product.name}, Size: {selected_size}, Quantity: {selected_quantity}, Total Price: €{total_item_price}")

        return redirect('cart')

    else:
        return redirect('cart')


def create_order(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    # Get the user's cart
    cart = Cart.objects.get(user=request.user)

    # Calculate the total price of the cart
    cart_total = cart.total_price()

    # You can calculate service_price and delivery_price based on user selections or some other logic
    service_price = 10.00  # Example value, replace it with actual logic
    delivery_price = 5.00  # Example value, replace it with actual logic

    # Create the order in the database
    order = Order.objects.create(
        user=request.user,
        total_price=cart_total,
        service_price=service_price,
        delivery_price=delivery_price
    )

    # Calculate the grand total of the order
    grand_total = order.get_grand_total()

    # Optionally, you can clear the cart after the order is placed
    cart.items.all().delete()  # Remove items from cart after creating the order

    # Return a summary of the order to the user
    return render(request, 'order_summary.html', {'order': order, 'grand_total': grand_total})