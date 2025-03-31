"""
Create models for Product and Category in Admin.
"""
from django.db import models


class Category(models.Model):
    """
    Create Categroy for search functionality in Admin and site
    """

    class Meta:
        verbose_name_plural = "Categories"
    """
    Adress plural error of Category in Admin
    """

    name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255, null=True, blank=True)
    subcategories = models.ManyToManyField(
        'self', blank=True,
        related_name='parent_categories', symmetrical=False)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    fallback_url = models.CharField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)


    def __str__(self):
        return str(self.name)


    def get_image(self):
        """ Image backup for Cloudinary (not yet implemented)"""
        if self.image_url:
            return self.image_url
        elif self.fallback_url:
            return self.fallback_url
        return '/path/to/default/image.jpg'
