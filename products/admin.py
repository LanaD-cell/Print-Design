from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Category

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

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

# Register the models with the admin
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)