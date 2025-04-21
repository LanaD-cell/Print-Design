from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


# Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField('image')

    def __str__(self):
        return self.name


# Product model
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=100)
    street_address1 = models.CharField(max_length=255)
    street_address2 = models.CharField(max_length=255, blank=True)

    # Optional delivery address fields
    delivery_country = models.CharField(max_length=100, blank=True)
    delivery_postcode = models.CharField(max_length=20, blank=True)
    delivery_town_or_city = models.CharField(max_length=100, blank=True)
    delivery_street_address1 = models.CharField(max_length=255, blank=True)
    delivery_street_address2 = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"