from django.db import models
from cloudinary.models import CloudinaryField

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