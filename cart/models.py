from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal

class Cart(models.Model):
    """
    Represents a user's shopping cart in the system.

    A cart stores a user's selected products along with their quantities
    and any associated information like size.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)

    def add_product(self, product, quantity, size=None):
        """
        Add a specified quantity of a product to the cart. If the product
        already exists in the cart, it updates the quantity. Otherwise,
        a new CartItem is created.

        """
        # Attempt to retrieve or create the CartItem
        cart_item, created = CartItem.objects.get_or_create(
            cart=self, product=product, size=size
        )

        if created:
            # If the item is new, initialize the price and total_price
            cart_item.price = product.price  # You can adjust if the price depends on size or quantity
            cart_item.total_price = cart_item.price * cart_item.quantity
        else:
            # If the item already exists, update the quantity and recalculate total price
            cart_item.quantity += quantity
            cart_item.total_price = cart_item.price * cart_item.quantity

        cart_item.save()

    def __str__(self):
        return f"Cart for {self.user}"

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

    # Optional: define service_price and delivery_price if necessary
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def total_price(self):
        """ Calculate total price of the item
        (product price * quantity + service and delivery) """
        return (self.product.price * self.quantity) + self.service_price + self.delivery_price

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

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
