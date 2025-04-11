from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Order
from decimal import Decimal


def view_cart(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the user's cart
    cart = Cart.objects.get(user=request.user)

    # Get the related CartItems
    cart_items = cart.items.all()

    # Use the method from the Cart model to calculate the total price
    total_price = cart.total_price()

    # Prepare the context to pass to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart/cart.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        print("POST data:", request.POST)

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        selected_size = request.POST.get('size')
        selected_quantity = int(request.POST.get('quantity_option'))
        selected_services = request.POST.getlist('services')
        selected_delivery = request.POST.get('delivery_options')

        if isinstance(selected_size, list):
            selected_size = selected_size[0]

        if isinstance(selected_quantity, list):
            selected_quantity = selected_quantity[0]

        selected_price = None
        for quantity in product.quantities:
            if quantity['quantity'] == selected_quantity:
                selected_price = Decimal(quantity['price'])
                break

        if selected_price is None:
            return redirect('cart:cart')

        # Define service and delivery prices
        servicePrices = {
            'own_print_data_option': Decimal('0.00'),
            'online_designs': Decimal('35.00'),
            'design_services': Decimal('40.00')
        }

        deliveryPrices = {
            'Standard Production': Decimal('5.00'),
            '48h Express Production': Decimal('10.00'),
            '24h Express Production': Decimal('15.00')
        }

        service_price = sum(servicePrices.get(service, Decimal('0.00')) for service in selected_services)
        delivery_price = deliveryPrices.get(selected_delivery, Decimal('0.00'))

        # Get or create the cart for the user
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Calculate the total item price
        total_item_price = selected_price + service_price + delivery_price

        # Create the CartItem without the total_price field
        cart_item = CartItem(
            cart=cart,
            product=product,
            size=selected_size,
            quantity=selected_quantity,
            price=selected_price,
            service_price=service_price,
            delivery_price=delivery_price
        )

        cart_item.save()

        # Update cart total price
        cart.total_price = cart.total_price()  # Recalculate total price
        cart.save()

        # Save cart data to session
        request.session['cart_id'] = cart.id

        # Debugging output
        print(f"Added to cart: {product.name}, Size: {selected_size}, Quantity: {selected_quantity}, Total Price: €{total_item_price}")
        print(f"Cart ID in session: {request.session.get('cart_id')}")

        return redirect('cart:cart_details')
    else:
        return redirect('cart:cart_details')


def create_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = Cart.objects.get(user=request.user)

    # Calculate service and delivery price based on cart items
    total_service_price = sum(item.service_price for item in cart.items.all())
    total_delivery_price = sum(item.delivery_price for item in cart.items.all())

    cart_total = cart.total_price  # Use the cart's total price

    order = Order.objects.create(
        user=request.user,
        total_price=cart_total,
        service_price=total_service_price,
        delivery_price=total_delivery_price
    )

    # Create order items
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.price,
            service_price=item.service_price,
            delivery_price=item.delivery_price
        )

    # Clear cart items after order creation
    cart.items.all().delete()

    grand_total = order.get_grand_total()

    return render(request, 'order_summary.html', {'order': order, 'grand_total': grand_total})

def remove_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart:cart_details')
