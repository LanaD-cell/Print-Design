# Generated by Django 5.1.7 on 2025-04-09 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_remove_productsize_customer_order_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
    ]
