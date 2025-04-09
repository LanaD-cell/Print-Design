from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'get_grand_total', 'status')
    inlines = [OrderItemInline]

    def status(self, obj):
        return "Pending"

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
