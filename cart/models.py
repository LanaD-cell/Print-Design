from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    """
    Represents a user's shopping cart in the system.

    A cart stores a user's selected products along with their quantities
    and any associated information like size.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_product(self, product, quantity, size=None):
        """
        Add a specified quantity of a product to the cart. If the product
        already exists in the cart, it updates the quantity. Otherwise,
        a new CartItem is created.

        """
        cart_item = CartItem.objects.get_or_create(
            cart=self, product=product, size=size
        )
        cart_item.quantity += quantity
        cart_item.save()

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    """
    Represents an individual item in a shopping cart, including the product,
    its size (if applicable), quantity, price, and total price.

    """
    cart = models.ForeignKey(
        Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.quantity}"
