# Generated by Django 3.1.5 on 2021-01-17 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default=None, max_length=15),
        ),
    ]
