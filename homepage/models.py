from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone


# Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField('image')

    def __str__(self):
        return str(self.name)


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return str(self.question)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(default='default@example.com')
    phone_number = models.CharField(max_length=20)
    street_address1 = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    # Optional delivery address fields
    delivery_country = models.CharField(max_length=100, blank=True)
    delivery_postcode = models.CharField(max_length=20, blank=True)
    delivery_town_or_city = models.CharField(max_length=100, blank=True)
    delivery_street_address1 = models.CharField(max_length=255, blank=True)
    delivery_street_address2 = models.CharField(max_length=255, blank=True)
    orders = models.ManyToManyField('checkout.Order', related_name='profiles', blank=True)
    purchased_products = models.ManyToManyField(
        Product, related_name='purchased_products', blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"  # pylint: disable=no-member


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)


class Newsletter(models.Model):
    PENDING = 'Pending'
    SENT = 'Sent'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    send_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return str(self.title)

    def mark_as_sent(self):
        """ Mark the newsletter as sent """
        self.status = self.SENT
        self.save()

    @property
    def status_display(self):
        """ Return a human-readable status for display """
        return (self.get_status_display())  # pylint: disable=no-member


class ContactRequest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact Request from {self.first_name} {self.last_name} ({self.email})"