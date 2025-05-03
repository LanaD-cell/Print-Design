from .models import FAQ
from allauth.account.models import EmailConfirmation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from checkout.models import Order
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.core.mail import send_mail
from .forms import SubscriberForm
from .models import Subscriber


def homepage(request):
    """ View to return Homepage and FAQ """
    faqs = FAQ.objects.all()
    return render(request, 'homepage/homepage.html', {'faqs': faqs})


@login_required
def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        user_orders = Order.objects.filter(user=user).order_by('-created_at')

        current_orders = user_orders.exclude(status__in=['Delivered', 'Cancelled'])
        previous_orders = user_orders.filter(status__in=['Delivered', 'Cancelled'])

        return render(request, 'profile/profile.html', {
            'current_orders': current_orders,
            'previous_orders': previous_orders,
        })

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    def get_success_url(self):
        return '/login-success/'

def login_success(request):
    """
    View to render the login success page.
    This page is shown after the user successfully logs in.
    """
    return render(request, 'registration/login_success.html')

def logout_view(request):
    logout(request)
    return redirect('logout-success')

def logout_success(request):
    """
    View to render the login success page.
    This page is shown after the user successfully logs in.
    """
    return render(request, 'registration/logout_success.html')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

def subscribe(request):
    """ Handle user subscription to the newsletter """
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Avoid duplicate subscriptions
            Subscriber.objects.get_or_create(email=email)
            messages.success(request, 'You have successfully subscribed to our newsletter!')
            form = SubscriberForm()  # Reset the form after success
    else:
        form = SubscriberForm()

    return render(request, 'newsletter/subscribe.html', {'form': form})

def send_newsletter(subject, message):
    recipients = [s.email for s in Subscriber.objects.all()]
    send_mail(subject, message, 'c.wnt.nd1053@gmail.com', recipients)

def subscribe_success(request):
    return render(request, 'subscribe_success.html')

def facebook_mockup(request):
    return render(request, 'mockups/facebook_mockup.html')
