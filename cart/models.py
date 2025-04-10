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
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # The price per unit of the product

    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.quantity}"

    def total_price(self):
        """
        Calculate the total price for the cart item.
        This includes the price of the product, any service price,
        delivery price, and the quantity.
        """
        return (self.price + self.service_price + self.delivery_price) * self.quantity

class Order(models.Model):
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)  # Add status field

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def get_grand_total(self):
        return self.total_price + self.service_price + self.delivery_price
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def total_price(self):
        return (self.price * self.quantity) + self.service_price + self.delivery_price
