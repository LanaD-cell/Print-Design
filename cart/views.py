from django.shortcuts import render, redirect

# View to return Cart
def view_cart(request):
    """ View to return Cart """
    return render(request, 'cart/cart.html')

# This view is for adding the product to the cart
def add_to_cart(request, product_id):
    """ Add a product to the cart """

    # Get quantity/size from the form, default to 1 if not provided
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('product_size')

    redirect_url = request.POST.get('redirect_url', 'view_cart')

    if not size:
        # If size is not selected and the product requires a size, handle it
        return redirect(redirect_url)  # Or show an error message

    # Get the cart from the session (if it exists)
    cart = request.session.get('cart', {})

    # Use product_id and size as a unique key for cart items
    cart_item_key = f"{product_id}_{size}"

    # If the item already exists in the cart, update the quantity
    if cart_item_key in cart:
        cart[cart_item_key]['quantity'] += quantity
    else:
        # Add the product with its size and quantity
        cart[cart_item_key] = {'product_id': product_id,
                               'quantity': quantity,
                               'size': size,
                               }

    # Update the cart in the session
    request.session['cart'] = cart

    # For debugging: Print the cart content
    print(request.session['cart'])

    return redirect(redirect_url)