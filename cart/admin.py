from django.contrib import admin
from .models import Cart, CartItem

# Inline for CartItem within CartAdmin
class CartItemInline(admin.TabularInline):
    model = CartItem
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

# Register the models with the admin site
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)

