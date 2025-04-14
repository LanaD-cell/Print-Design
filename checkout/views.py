from django.shortcuts import render

# Create your views here.
def create_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = Cart.objects.get(user=request.user)

    # Calculate service and delivery price based on cart items
    total_service_price = sum(
        item.service_price for item in cart.items.all())
    total_delivery_price = sum(
        item.delivery_price for item in cart.items.all())

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

    return render(
        request, 'order_summary.html', {
            'order': order, 'grand_total': grand_total})
