from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (Product,
                    Category,
                    ProductSize,
                    QuantityOption)


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class QuantityOptionInline(admin.TabularInline):
    model = QuantityOption
    extra = 1

class ProductAdmin(SummernoteModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'image',
        'rating',
    )

    ordering = ('name',)

    # Add Summernote editor for 'description' field
    summernote_fields = ('description',)

    # Include ProductSize inline form to manage
    # sizes and quantities directly in the
    # Product admin
    inlines = [ProductSizeInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

# Register the models with the admin
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductSize)
admin.site.register(QuantityOption)