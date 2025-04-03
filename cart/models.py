from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_product(self, product, quantity, size=None):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self, product=product, size=size
        )
        cart_item.quantity += quantity
        cart_item.save()

    def __str__(self):
        return f"Cart for {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
