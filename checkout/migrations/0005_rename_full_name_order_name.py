# Generated by Django 5.1.7 on 2025-04-15 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_order_additional_services_order_service_cost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='full_name',
            new_name='name',
        ),
    ]
