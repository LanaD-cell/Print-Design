from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (Product,
                    Category,
                    ProductSize,
                    QuantityOption)
from django import forms


class QuantityOptionForm(forms.ModelForm):
    class Meta:
        model = QuantityOption
        fields = ['quantity', 'price']

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        price = cleaned_data.get('price')

        if not quantity or not price:
            raise forms.ValidationError("Both quantity and price must be provided.")

        # Ensure price is greater than zero
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")

        return cleaned_data


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


class QuantityOptionInline(admin.TabularInline):
    model = QuantityOption
    form = QuantityOptionForm
    extra = 1
    fields = ['quantity', 'price']


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

    inlines = [ProductSizeInline, QuantityOptionInline]

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
admin.site.register(ProductSize)
admin.site.register(QuantityOption)