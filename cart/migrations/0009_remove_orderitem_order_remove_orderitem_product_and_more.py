# Generated by Django 5.1.7 on 2025-04-14 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
