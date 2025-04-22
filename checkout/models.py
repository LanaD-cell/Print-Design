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

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    order_number = models.CharField(
        max_length=32, null=False, editable=False)
    name = models.CharField(
        max_length=50, null=False, blank=False)
    email = models.EmailField(
        max_length=254, null=False, blank=False)
    phone_number = models.CharField(
        max_length=20, null=False, blank=False)
    country = models.CharField(
        max_length=40, null=False, blank=False)
    postcode = models.CharField(
        max_length=20, null=True, blank=True)
    town_or_city = models.CharField(
        max_length=40, null=False, blank=False)
    street_address1 = models.CharField(
        max_length=80, null=False, blank=False)
    street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    delivery_option = models.CharField(
        max_length=100,
        choices=[('standard production', 'Standard Production'),
                 ('priority delivery', 'Priority Delivery'),
                 ('48h express delivery', '48h Express Delivery'),
                 ('24h express delivery', '24h Express Delivery')],
        default='standard')
    print_data_file = models.FileField(
        upload_to='print_uploads/', null=True, blank=True)
    save_info = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True)
    items = models.ManyToManyField(
        'cart.CartItem', related_name='orders_items')
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)

    service_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    additional_services = models.JSONField(default=list)
    service_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        print("Updating total for order:", self.order_number)

        # pylint: disable=no-member
        self.order_total = self.items.all().aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0

        # Calculate the service cost
        self.additional_services = self.additional_services or []

        # If the total = 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
        else:
            self.delivery_cost = 0

        self.grand_total = (
            self.order_total + self.delivery_cost + self.service_cost
        )

        print(
            "Updated totals -> order_total:", self.order_total,
            "service_cost:", self.service_cost,
            "delivery_cost:", self.delivery_cost,
            "grand_total:", self.grand_total
        )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

        # Update the total without causing recursion
        self.update_total()

        print(f"Saving Order {self.order_number}, Total: {self.grand_total}")

        # Now save the order instance
        super().save(*args, **kwargs)

    def __str__(self):
        # pylint: disable=no-member
        return f"Order #{self.order_number} - {self.user.username}"

    def total_price(self):
        """
        Calculate the total price for the order.
        This includes the price of all OrderItems,
        along with service and delivery costs.
        """
        # pylint: disable=no-member
        return sum(item.total_price() for item in self.items.all())

    def get_grand_total(self):
        return self.total_price() + self.service_price + self.delivery_price


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="line_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=False, blank=False, editable=False)
    service_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    delivery_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    additional_services = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        total_price = 0
        # pylint: disable=no-member
        if self.product.quantities:
            quantities = self.product.quantities or []
            # Look for the exact quantity in the JSON
            for qty in quantities:
                if self.quantity == qty["quantity"]:
                    total_price = qty["price"]
                    break

        # If no price found in JSON, we might want to handle it
        if total_price == 0:
            raise ValueError(
                f"No price found for quantity {self.quantity} in "
                "product pricing."
            )

        # Add service and delivery prices to the total
        self.lineitem_total = (
            Decimal(total_price) + self.service_price + self.delivery_price
        )
        super().save(*args, **kwargs)

    def __str__(self):
        # pylint: disable=no-member
        return (
            f"Product ID {self.product.id} on order "
            f"{self.order.order_number}"
        )

    def total_price(self):
        # Calculate total price without multiplying by quantity
        return self.lineitem_total
