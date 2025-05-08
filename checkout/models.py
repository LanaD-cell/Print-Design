import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.conf import settings
from products.models import Product


def get_superuser():
    return User.objects.get(is_superuser=True).id


class Order(models.Model):
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    PAID = 'paid'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]

    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null = True, blank = True)
    complete = models.BooleanField(default=False)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=5.00)

    save_info = models.BooleanField(default=False)

    items = models.ManyToManyField('cart.CartItem', related_name='orders_items')
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    service_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    additional_services = models.JSONField(default=list)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def get_grand_total(self):
        """Returns the grand total (sum of order total, service cost, and delivery cost)."""
        return self.order_total + self.service_cost + self.delivery_cost

    def _generate_order_number(self):
        """Generate a unique order number."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update totals for the order."""
        self.order_total = self.line_items.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.delivery_cost = 5.00
        self.grand_total = self.order_total + self.service_cost + self.delivery_cost

    def save(self, *args, **kwargs):
        """Override save method to ensure order number is set and totals are updated."""
        if not self.order_number:
            self.order_number = self._generate_order_number()

        # First save to ensure PK exists
        super().save(*args, **kwargs)

        # Update totals only after the instance is saved and has a PK
        self.update_total()

        # Save only the updated total fields
        super().save(update_fields=["order_total", "grand_total", "delivery_cost"])

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"

    def total_price(self):
        """Return the total price for all items in the order."""
        return sum(item.total_price() for item in self.items.all())



class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="line_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    additional_services = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        """Override save to ensure correct pricing."""
        total_price = Decimal(0)

        # Find the price corresponding to the quantity
        if self.product.quantities:
            quantities = self.product.quantities or []
            for qty in quantities:
                if self.quantity == qty["quantity"]:
                    total_price = qty["price"]
                    break

        if total_price == 0:
            raise ValueError(f"No price found for quantity {self.quantity} in product pricing.")

        # Calculate the lineitem total
        self.lineitem_total = total_price + self.service_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product ID {self.product.id} on order {self.order.order_number}"

    def total_price(self):
        """Return the total price for this line item."""
        return self.lineitem_total
