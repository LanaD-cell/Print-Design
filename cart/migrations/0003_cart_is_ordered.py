# Generated by Django 5.1.7 on 2025-04-08 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cart_updated_at_cartitem_price_cartitem_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
    ]
