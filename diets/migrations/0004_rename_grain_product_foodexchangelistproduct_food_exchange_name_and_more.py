# Generated by Django 5.0.7 on 2024-08-03 16:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("diets", "0003_alter_diet_diet_set"),
    ]

    operations = [
        migrations.RenameField(
            model_name="foodexchangelistproduct",
            old_name="grain_product",
            new_name="food_exchange_name",
        ),
        migrations.RenameField(
            model_name="foodexchangelistproduct",
            old_name="dairy_product",
            new_name="product",
        ),
        migrations.RemoveField(
            model_name="foodexchangelistproduct",
            name="fat_product",
        ),
        migrations.RemoveField(
            model_name="foodexchangelistproduct",
            name="fish_meat_low_fat_product",
        ),
        migrations.RemoveField(
            model_name="foodexchangelistproduct",
            name="fish_meat_medium_fat_product",
        ),
        migrations.RemoveField(
            model_name="foodexchangelistproduct",
            name="fruit_product",
        ),
        migrations.RemoveField(
            model_name="foodexchangelistproduct",
            name="vegetable_product",
        ),
    ]
