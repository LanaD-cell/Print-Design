from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from homepage.models import PrintData
from django.contrib import messages
from decimal import Decimal
import json


def view_cart(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the user's cart
    cart = Cart.objects.get(user=request.user)

    # Get the related CartItems
    cart_items = cart.items.all()

    for item in cart_items:
        try:
            item.services = json.loads(item.services)
        except (json.JSONDecodeError, TypeError):
            item.services = []

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

        # Handle the case where size or quantity might be in a list format
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

        servicePrices = {
            'Own Print Data Upload': Decimal('0.00'),
            'Online Designer': Decimal('35.00'),
            'Design Service': Decimal('40.00'),
            'Standard Production': Decimal('0.00'),
            'Priority Production': Decimal('15.00'),
            '48h Express Production': Decimal('25.00'),
            '24h Express Production': Decimal('35.00'),
        }

        # Debugging purpose
        print(request.POST)

        # Map the selected services to their corresponding price values
        service_price = sum(
            servicePrices.get(service, Decimal('0.00')) for service in selected_services)

        # Handle the 'Own Print Data Upload' service, if selected
        if 'Own Print Data Upload' in selected_services and 'print_data_file' in request.FILES:
            file = request.FILES['print_data_file']


        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Show an error message
            messages.error(request, "Please sign up or log in to upload print data.")

            # Redirect to the login page
            return redirect('login')

            # Create a PrintData object and link it to the user
            print_data = PrintData.objects.create(
                user=request.user,
                product=product,
                uploaded_file=file,
                service_type='Own Print Data Upload'
            )

            request.user.profile.print_data_files.add(print_data)
            request.user.profile.save()

            messages.success(request, f"Print data uploaded: {file.name} for product {product.name}")

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            # Handle guest users (non-authenticated)
            cart_id = request.session.get('cart_id')
            if not cart_id:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
            else:
                cart = Cart.objects.get(id=cart_id)

        # Create the CartItem object
        cart_item = CartItem(
            cart=cart,
            product=product,
            size=selected_size,
            quantity=selected_quantity,
            price=selected_price,
            service_price=service_price,
            services=json.dumps(selected_services),
        )

        # Properly handle the services field here
        try:
            cart_item.services = json.loads(cart_item.services)
        except (json.JSONDecodeError, TypeError):
            cart_item.services = []

        cart_item.save()

        # Update the cart's total price
        cart.total_price = cart.total_price()
        cart.save()

        # Save cart data to session
        request.session['cart_id'] = cart.id

        # Debugging output
        print(
            f"Added to cart: {product.name}, Size: {selected_size}, "
            f"Quantity: {selected_quantity}, Price: €{selected_price}, "
            f"Service Price: €{service_price}")
        print(f"Cart ID in session: {request.session.get('cart_id')}")

        messages.success(request, "Item added to your Cart!")

        return redirect('cart:cart_details')
    else:
        return redirect('cart:cart_details')

def remove_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        messages.info(request, 'Item removed from Cart.')
    except CartItem.DoesNotExist:
        pass

    return redirect('cart:cart_details')
