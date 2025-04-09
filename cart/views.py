from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from products.models import Product, ProductSize, QuantityOption
from .models import Cart, CartItem, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError


@login_required
def view_cart(request):
    # Retrieve the cart from the session (if any)
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = Decimal('0.00')

    # Iterate through the cart items
    for item in cart.values():
        try:
            # Get the price for the selected quantity
            price = Decimal(str(item['price']))  # No multiplication needed; this price is already for the selected quantity
            service_price = Decimal(str(item['service_price']))
            delivery_price = Decimal(str(item['delivery_price']))
            quantity = item['quantity']

            # Calculate the subtotal for each product
            subtotal = price + service_price + delivery_price
            grand_total += subtotal  # Add to the grand total

            # Append the item details for the cart
            cart_items.append({
                'product_name': item['product_name'],
                'price': price,
                'quantity': quantity,
                'total_price': subtotal,
                'service_price': service_price,
                'delivery_price': delivery_price,
            })
        except (KeyError, ValueError, TypeError, ValidationError):
            # Handle any unexpected errors gracefully
            continue

    # Return the cart items and grand total to the template
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
    })

def add_to_cart(request, product_id):
    # Get the product object from the database
    product = get_object_or_404(Product, id=product_id)

    # Get selected quantity and pricing options from the POST data
    selected_quantity = request.POST.get('quantity_option')  # e.g., '25'
    service_price = request.POST.get('services', '0')  # Default to '0' if not provided
    delivery_price = request.POST.get('delivery_option', '0')  # Default to '0' if not provided

    # Debugging the received values
    print(f"Selected Quantity: {selected_quantity}, Service Price: {service_price}, Delivery Price: {delivery_price}")

    try:
        # Convert selected quantity to integer
        selected_quantity = int(selected_quantity)
        # Convert service_price and delivery_price to float, defaulting to 0.0 if empty string
        service_price = float(service_price) if service_price != '' else 0.0
        delivery_price = float(delivery_price) if delivery_price != '' else 0.0
    except (ValueError, TypeError) as e:
        # If there's a conversion error, return an error response
        print(f"Error during conversion: {e}")
        return JsonResponse({'success': False, 'error': 'Invalid input'}, status=400)

    # Get the correct price from the quantities JSON field
    matched_price = next(
        (q['price'] for q in product.quantities if q['quantity'] == selected_quantity),
        None
    )

    # If no matched price is found, return an error response
    if matched_price is None:
        print(f"Price not found for selected quantity: {selected_quantity}")
        return JsonResponse({'success': False, 'error': 'Price not found for selected quantity'}, status=400)

    # Debugging the matched price
    print(f"Matched Price for Quantity {selected_quantity}: {matched_price}")

    # Initialize the cart if it doesn't exist
    if 'cart' not in request.session or not isinstance(request.session['cart'], dict):
        request.session['cart'] = {}

    # Add the product to the cart with the selected quantity and price
    request.session['cart'][str(product.id)] = {
        'product_name': product.name,
        'product_id': product.id,
        'quantity': selected_quantity,
        'price': float(matched_price),  # Using the matched price from quantities
        'service_price': service_price,
        'delivery_price': delivery_price,
    }

    # Mark the session as modified
    request.session.modified = True

    return redirect('cart')  # Redirect to the cart page


def adjust_cart(request, item_id):
    """ Adjust quantity of a cart item """
    size = request.POST.get('product_size')
    new_quantity = int(request.POST.get('quantity'))

    cart_items = request.session.get('cart', [])

    for item in cart_items:
        if item['product_id'] == int(item_id) and item['size'] == size:
            if new_quantity > 0:
                item['quantity'] = new_quantity
                item['total_price'] = float(item['price']) * new_quantity
                messages.success(request, f"Updated {item['name']} ({size}) quantity to {new_quantity}")
            else:
                cart_items.remove(item)
                messages.success(request, f"Removed {item['name']} ({size}) from your cart")
            break

    request.session['cart'] = cart_items
    request.session.modified = True

    return redirect('view_cart')


def remove_from_cart(request, item_id):
    """ Remove item from the cart completely """
    size = request.POST.get('product_size')
    cart_items = request.session.get('cart', [])

    for item in cart_items:
        if item['product_id'] == int(item_id) and item['size'] == size:
            cart_items.remove(item)
            messages.success(request, f"Removed {item['name']} ({size}) from your cart")
            break

    request.session['cart'] = cart_items
    request.session.modified = True

    return HttpResponse(status=200)

def checkout(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the cart from the session
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')  # If the cart is empty, redirect back to the cart page

    # Create the order
    order = Order.objects.create(
        user=request.user,
        total_price=0,  # We will calculate this below
        service_price=0,
        delivery_price=0,
    )

    # Add items to the order
    total_price = 0
    service_price = 0
    delivery_price = 0

    for item in cart.values():
        product = Product.objects.get(id=item['product_id'])  # Assuming `product_id` is stored in the cart
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=item['price'],
            service_price=item['service_price'],
            delivery_price=item['delivery_price'],
        )
        total_price += item['price'] * item['quantity']
        service_price += item['service_price']
        delivery_price += item['delivery_price']

    # Update the total prices in the order
    order.total_price = total_price
    order.service_price = service_price
    order.delivery_price = delivery_price
    order.save()

    # Clear the cart from the session
    del request.session['cart']

    return redirect('order_detail', order_id=order.id)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})