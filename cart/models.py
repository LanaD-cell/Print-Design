from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_option = models.CharField(max_length=255, null=True, blank=True)

    def items_subtotal(self):
        """Subtotal before VAT and delivery (just items and services)."""
        return sum(item.total_price() for item in self.items.all())

    def get_delivery_price(self):
        """Returns delivery price based on the selected option."""
        if not self.delivery_option:
            return Decimal('0.00')

        if self.delivery_option == 'Standard Production':
            return Decimal('0.00')
        elif self.delivery_option == '48h Express Production':
            return Decimal('15.00')
        elif self.delivery_option == '24h Express Production':
            return Decimal('25.00')
        elif self.delivery_option == '24h Express Delivery':
            return Decimal('35.00')

        return Decimal('0.00')

    def calculate_vat(self, subtotal):
        """Calculate VAT (19%) on the subtotal (not including delivery)."""
        return subtotal * Decimal('0.19')

    def grand_total(self):
        """Final total: items + VAT + delivery."""
        subtotal = self.items_subtotal()
        vat = self.calculate_vat(subtotal)
        delivery = self.get_delivery_price()
        return subtotal + vat + delivery

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
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
        and the quantity.
        """
        return (Decimal(self.price or 0) + Decimal(self.service_price or 0))

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.is_service and self.service_price <= 0:
            raise ValidationError("Service price must be greater than zero for services.")
