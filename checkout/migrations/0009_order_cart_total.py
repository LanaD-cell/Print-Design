# Generated by Django 5.1.7 on 2025-05-05 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_printdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
