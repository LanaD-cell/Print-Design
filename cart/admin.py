from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

# Inline for CartItem within CartAdmin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

# Inline for OrderItem within OrderAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# Cart Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_price')
    inlines = [CartItemInline]

    # Custom action to empty cart
    actions = ['empty_cart']

    def empty_cart(self, request, queryset):
        for cart in queryset:
            cart.items.all().delete()
            self.message_user(request, f"Cart for {cart.user.username} has been emptied.")

    empty_cart.short_description = "Empty selected carts"

# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'get_grand_total', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]

    # Customize the 'status' field to be a dropdown list
    def status(self, obj):
        return obj.get_status_display()


    actions = ['mark_as_shipped', 'mark_as_delivered']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status=Order.SHIPPED)
        self.message_user(request, "Selected orders have been marked as Shipped.")

    def mark_as_delivered(self, request, queryset):
        queryset.update(status=Order.DELIVERED)
        self.message_user(request, "Selected orders have been marked as Delivered.")

    mark_as_shipped.short_description = "Mark selected orders as Shipped"
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

# Register the models with the admin site
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem)
admin.site.register(OrderItem)
