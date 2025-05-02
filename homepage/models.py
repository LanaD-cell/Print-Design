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


# For storing user-uploaded files
class PrintData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="print_data")
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_file = models.FileField(upload_to='user_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    service_type = models.CharField(max_length=100, choices=[
        ('Own Print Data Upload', 'Own Print Data Upload'),
        ('Online Designer', 'Online Designer'),
        ('Design Service', 'Design Service'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.product.name if self.product else 'No Product'}"

    class Meta:
        verbose_name = "Print Data"
        verbose_name_plural = "Print Data Entries"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    print_data_files = models.ManyToManyField(PrintData, blank=True, related_name='profiles')

    def __str__(self):
        return f"Profile for {self.user.username}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email