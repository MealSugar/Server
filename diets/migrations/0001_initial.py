# Generated by Django 5.0.7 on 2024-07-22 08:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodExchangeListCalorie',
            fields=[
                ('food_exchange_list_calorie_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('energy_calorie', models.IntegerField(default=0)),
                ('grain', models.IntegerField(default=0)),
                ('fish_meat_low_fat', models.IntegerField(default=0)),
                ('fish_meat_medium_fat', models.IntegerField(default=0)),
                ('fruit', models.IntegerField(default=0)),
                ('fat', models.IntegerField(default=0)),
                ('dairy', models.IntegerField(default=0)),
                ('vegetable', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FoodExchangeListProduct',
            fields=[
                ('food_exchange_list_product_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('grain_product', models.CharField(max_length=100)),
                ('fish_meat_low_fat_product', models.TextField()),
                ('fish_meat_medium_fat_product', models.TextField()),
                ('fruit_product', models.TextField()),
                ('fat_product', models.TextField()),
                ('dairy_product', models.TextField()),
                ('vegetable_product', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DietSet',
            fields=[
                ('diet_set_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dietsets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('diet_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('diet_name', models.CharField(blank=True, max_length=100, null=True)),
                ('diet_calorie', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('diet_img', models.ImageField(blank=True, null=True, upload_to='diet_photo/%Y%m%d')),
                ('meal_time', models.CharField(blank=True, max_length=100, null=True)),
                ('meal_type', models.CharField(blank=True, max_length=100, null=True)),
                ('is_my_recipe', models.BooleanField(default=False)),
                ('is_like', models.BooleanField(default=False)),
                ('heart_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diets', to=settings.AUTH_USER_MODEL)),
                ('diet_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diets', to='diets.dietset')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('food_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('food_name', models.CharField(max_length=100)),
                ('food_type', models.CharField(max_length=100)),
                ('food_calorie', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('recipe', models.TextField()),
                ('grain', models.IntegerField(default=0)),
                ('fish_meat_low_fat', models.IntegerField(default=0)),
                ('fish_meat_medium_fat', models.IntegerField(default=0)),
                ('fruit', models.IntegerField(default=0)),
                ('fat', models.IntegerField(default=0)),
                ('dairy', models.IntegerField(default=0)),
                ('vegetable', models.IntegerField(default=0)),
                ('diet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foods', to='diets.diet')),
            ],
        ),
    ]
