from django.contrib import admin
from .models import Order, OrderItem

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['price', 'service_price', 'delivery_price']
    extra = 0  # Controls how many extra forms are displayed

class OrderAdmin(admin.ModelAdmin):
    # Correctly order by the 'created_at' field on the Order model
    ordering = ['created_at']

    # Display fields for the Order model, not OrderItem
    list_display = ['order_number', 'created_at', 'user', 'status', 'order_total']

    # Fields to be displayed as read-only in the Order admin
    readonly_fields = ['order_number', 'created_at', 'status', 'order_total']

    inlines = [OrderItemAdmin]  # Use the inline for OrderItem

admin.site.register(Order, OrderAdmin)