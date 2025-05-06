from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        """
        Calculate the total price for all items in the cart.
        This uses the `total_price` method from the CartItem model.
        """
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """
    Represents an individual item in a shopping cart, including the product,
    its size (if applicable), quantity, price, and total price.
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_service = models.BooleanField(default=False)
    services = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.quantity}"

    def total_price(self):
        """
        Calculate the total price for the cart item.
        This includes the price of the product, any service price,
        delivery price, and the quantity.
        """
        return (
            Decimal(self.price or 0) + Decimal(self.service_price or 0)
        )

    def save(self, *args, **kwargs):
        if self.is_service and self.service_price <= 0:
            raise ValueError("Service price must be greater than zero for services.")
        super().save(*args, **kwargs)

