from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem
from django.conf import settings
import stripe
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
        selected_services = request.POST.getlist('services')

        # Handle the case where size or quantity might be in a list format
        if isinstance(selected_size, list):
            selected_size = selected_size[0]

        selected_quantity_str = request.POST.get('quantity_option', '')

        # Validate that the quantity is a valid integer
        try:
            if selected_quantity_str:
                selected_quantity = int(selected_quantity_str)
            else:
                selected_quantity = 1
        except ValueError:
            messages.error(request, "Invalid quantity selected.")
            return redirect('cart:cart')

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
            servicePrices.get(
                service, Decimal('0.00')) for service in selected_services)

        # Handle the 'Own Print Data Upload' service, if selected
        file = None
        if 'Own Print Data Upload' in selected_services and \
                'print_data_file' in request.FILES:
            file = request.FILES['print_data_file']

        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Show an error message
            messages.error(
                request, "Please sign up or log in to upload print data.")

            # Redirect to the login page
            return redirect('login')

        # Create a PrintData object and link it to the user, only if a file was uploaded
        if file:
            print_data = PrintData.objects.create(
                user=request.user,
                product=product,
                uploaded_file=file,
                service_type='Own Print Data Upload'
            )

            request.user.profile.print_data_files.add(print_data)
            request.user.profile.save()

            messages.success(request, f"Print data uploaded: {file.name} for product {product.name}")

        # Check if the user is authenticated and get the cart
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


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session():
  session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f"Order #{order_number}",
                        },
                        'unit_amount': int(grand_total * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://your-site.com/success',
                cancel_url='https://your-site.com/cancel',
            )

  return redirect(session.url, code=303)

if __name__== '__main__':
    app.run(port=4242)


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


def payment_cancel(request):
    return render(request, 'checkout/cancel.html')


def checkout_success_page(request, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        order_id = session.client_reference_id
        order = get_object_or_404(Order, id=order_id)
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e.user_message}")
        messages.error(request, "An error occurred while processing the payment.")
        return redirect('checkout:summary')
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        messages.error(request, "An unexpected error occurred.")
        return redirect('checkout:summary')

    return render(request, 'checkout/order_summary.html', {'order': order})


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

@login_required
def payment_success(request, order_number):
    session_id = request.GET.get('session_id')

    if not session_id:
        messages.error(request, "Session ID missing!")
        return redirect('checkout:order_summary')

    try:
        # Retrieve the Stripe session using the session ID
        session = stripe.checkout.Session.retrieve(session_id)

        # Get the associated order using the order_number
        order = get_object_or_404(Order, order_number=order_number)

        # Check if the session corresponds to the order
        if order.order_number != session.client_reference_id:
            messages.error(request, "Order number mismatch!")
            return redirect('checkout:order_summary')

        # If payment was successful, update the order status and save the order
        if session.payment_status == 'paid':
            order.status = 'Paid'
            order.save()

            # Now, link the order products to the user's profile
            user = request.user
            products = order.products.all()

            for product in products:
                user.purchased_products.add(product)

            # Optionally, clear the cart after the purchase is successful
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True

            # Success message
            messages.success(request, f"Payment successful! Your order number is {order_number}.")

            # Render success page
            return render(request, 'checkout/success.html', {'order': order})

        else:
            # If payment failed
            messages.error(request, "Payment failed. Please try again.")
            return redirect('checkout:order_checkout')

    except Exception as e:
        # Catch any errors that occur during the process
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('checkout:order_summary')

