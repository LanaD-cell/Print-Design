from .models import FAQ
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from checkout.models import Order

def homepage(request):
    """ View to return Homepage and FAQ """
    faqs = FAQ.objects.all()
    return render(request, 'homepage/homepage.html', {'faqs': faqs})


@login_required
def profile_view(request):
    user = request.user
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    current_orders = user_orders.exclude(status__in=['Delivered', 'Cancelled'])
    previous_orders = user_orders.filter(status__in=['Delivered', 'Cancelled'])

    return render(request, 'profile/profile.html', {
        'current_orders': current_orders,
        'previous_orders': previous_orders,
    })