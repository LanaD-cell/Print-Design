from .models import FAQ
from django.views.decorators.csrf import csrf_exempt
from allauth.account.models import EmailConfirmation
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from checkout.models import Order
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.core.mail import send_mail
from .forms import SubscriberForm, ContactRequestForm
from .models import Subscriber, FAQ, ContactRequest
from cart.models import Cart


def homepage(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    else:
        cart_items = []

    faqs = FAQ.objects.all()

    return render(request, 'homepage/homepage.html', {
        'cart_items': cart_items,
        'faqs': faqs,
    })


@login_required
def profile_view(request):
    if request.user.is_authenticated:
        user = request.user

        user_orders = Order.objects.filter(
            user=user
        ).order_by('-created_at')

        current_orders = user_orders.exclude(
            status__in=['Delivered', 'Cancelled']
        )
        previous_orders = user_orders.filter(
            status__in=['Delivered', 'Cancelled']
        )

        # Debugging output
        print("Current Orders:", current_orders)
        print("Previous Orders:", previous_orders)

        return render(request, 'profile/profile.html', {
            'current_orders': current_orders,
            'previous_orders': previous_orders,
        })


class CustomLoginView(LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        return '/login-success/'


@login_required
def login_success(request):
    return render(request, 'registration/login_success.html')


def logout_view(request):
    logout(request)
    return redirect('logout-success')


def logout_success(request):
    return render(request, 'registration/logout_success.html')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)


def subscribe(request):
    """Handle user subscription to the newsletter"""
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            Subscriber.objects.get_or_create(email=email)
            messages.success(
                request,
                'You have successfully subscribed to our newsletter!',
                extra_tags="subscription"
            )
            form = SubscriberForm()
            return redirect('subscribe')
    else:
        form = SubscriberForm()

    return render(request, 'newsletter/subscribe.html', {'form': form})


def send_newsletter(subject, message):
    recipients = [s.email for s in Subscriber.objects.all()]
    send_mail(subject, message, 'c.wnt.nd1053@gmail.com', recipients)


def facebook_mockup(request):
    return render(request, 'mockups/facebook_mockup.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact = ContactRequest(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message'],
            )
            contact.save()

            send_mail(
                'New contact form message',
                f"Message from {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}:\n\n{form.cleaned_data['message']}",
                form.cleaned_data['email'],
                [settings.DEFAULT_FROM_EMAIL],
            )

            return redirect('homepage:contact_success')
        else:
            return render(request, 'contact/contact.html', {'form': form})
    else:
        form = ContactRequestForm()
        return render(request, 'contact/contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'contact/contact_success.html')