# Generated by Django 5.1.7 on 2025-04-10 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_remove_product_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='additional_services',
            field=models.JSONField(blank=True, default=list, max_length=1024),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantities',
            field=models.JSONField(blank=True, default=list, max_length=1024),
        ),
        migrations.AlterField(
            model_name='product',
            name='sizes',
            field=models.JSONField(blank=True, default=list, max_length=1024),
        ),
    ]
