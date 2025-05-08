from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Category
from django import forms


class ProductAdmin(SummernoteModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'category',
        'image',
        'rating',
    )

    ordering = ('name',)

    # Add Summernote editor for 'description' field
    summernote_fields = ('description',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

    search_fields = ('name', 'friendly_name')


# Register the models with the admin
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
