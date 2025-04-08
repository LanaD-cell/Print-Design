from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from products.models import Product, ProductSize, QuantityOption
from cart.models import Cart
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser

@login_required
# View to return Cart
def view_cart(request):
    """ View to return Cart """
    cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'cart/cart.html', {'cart': cart})


# This view is for adding the product to the cart
def add_to_cart(request, product_id):
    """ Add a quantity of the specified product to the shopping bag """
    product = Product.objects.get(id=product_id)
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity_option'))

    product_size = product.product_sizes.get(size=size)
    quantity_option = product_size.quantity_options.get(quantity=quantity)

    # Create a new cart if no cart exists
    if 'cart' not in request.session:
        request.session['cart'] = []

    cart_items = request.session['cart']

    for item in cart_items:
        if item['product_id'] == product.id and item['size'] == size:
            item['quantity'] += quantity
            item['total_price'] = item['quantity'] * float(item['price'])
            break
    else:
        # Add new item to cart
        cart_items.append({
            'product_id': product.id,
            'name': product.name,
            'size': size,
            'quantity': quantity,
            'price': str(quantity_option.price),
            'total_price': str(quantity_option.price * quantity),
        })

    # Save cart, retunr to session
    request.session['cart'] = cart_items
    request.session.modified = True

    return redirect('product_detail', product_id=product.id)


def adjust_cart(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    cart = request.session.get('cart', {})
    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(
                request,
                f'Updated size {size.upper()} {product.name} quantity to '
                f'{cart[item_id]["items_by_size"][size]}'
            )
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(
                request,
                f'Removed size {size.upper()} {product.name} from your cart'
            )
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(
                request,
                f'Updated {product.name} quantity to {cart[item_id]}'
            )
        else:
            cart.pop(item_id)
            messages.success(
                request,
                f'Removed {product.name} from your cart'
            )

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """ Remove the item from the shopping bag """

    product = get_object_or_404(Product, pk=item_id)

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(
                request,
                f'Removed size {size.upper()} {product.name} from your cart'
            )
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)