# Generated by Django 5.0.7 on 2024-08-05 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diets', '0004_rename_grain_product_foodexchangelistproduct_food_exchange_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diet',
            name='is_certificated',
            field=models.BooleanField(default=False),
        ),
    ]
