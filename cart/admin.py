from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'grand_total_display')
    inlines = [CartItemInline]
    actions = ['empty_cart']

    def empty_cart(self, request, queryset):
        for cart in queryset:
            cart.items.all().delete()
            self.message_user(request, f"Cart for {cart.user.username} has been emptied.")
    empty_cart.short_description = "Empty selected carts"

    def grand_total_display(self, obj):
        return obj.grand_total()
    grand_total_display.short_description = 'Grand Total'

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
