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


class ProductSize(models.Model):
    """
    Add Sizes and Quantities for each product
    """
    product = models.ForeignKey(
        'Product', related_name='product_sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class QuantityOption(models.Model):
    """
    Stores predefined quantity options and their
    prices, associated with a product size.
    """
    product = models.ForeignKey(
        'Product', related_name='quantity_options', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} @ €{self.price} netto"


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

    # New Fields
    sizes = models.JSONField(default=list, blank=True)
    quantities = models.JSONField(default=list, blank=True)
    additional_services = models.JSONField(default=list, blank=True)

    def __str__(self):
        return str(self.name)

    def get_image(self):
        """ Image backup for Cloudinary """
        if self.image_url:
            return self.image_url
        elif self.fallback_url:
            return self.fallback_url
        return '/path/to/default/image.jpg'

    def get_sizes(self):
        """Returns a list of sizes, split by commas."""
        return self.sizes.split(',') if self.sizes else []

    def get_quantities(self):
        """Returns a list of quantities and their prices for this product."""
        return [(quantity.quantity, quantity.price) for quantity in self.quantities.all()] if self.quantities.exists() else []
