from django.contrib import admin
from .models import Order, OrderLineItem

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    # Correctly order by the 'created_at' field on the Order model
    ordering = ['created_at']

    # Display fields for the Order model, not OrderItem
    list_display = ('order_number', 'created_at', 'name',
                    'order_total', 'delivery_cost', 'service_cost',
                    'grand_total',)

    # Fields to be displayed as read-only in the Order admin
    readonly_fields = ('order_number', 'created_at',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    fields = ('order_number', 'created_at', 'name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'service_cost', 'delivery_cost',
              'order_total', 'grand_total',)

    inlines = [OrderLineItemAdminInline]

admin.site.register(Order, OrderAdmin)
