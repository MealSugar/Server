from django.db import models
from django.conf import settings


class DietSet(models.Model):
    diet_set_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dietsets')
    created_at = models.DateField(auto_now_add=True)


class Diet(models.Model):
    diet_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diets')
    diet_set = models.ForeignKey(DietSet, on_delete=models.CASCADE, related_name='diets', blank=True, null=True)
    diet_name = models.CharField(max_length=100, blank=True, null=True)
    diet_calorie = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    diet_img = models.ImageField(upload_to='diet_photo/%Y%m%d', blank=True, null=True)
    meal_time = models.CharField(max_length=100, blank=True, null=True)
    meal_type = models.CharField(max_length=100, blank=True, null=True)
    is_my_recipe = models.BooleanField(default=False)
    is_like = models.BooleanField(default=False)
    heart_count = models.IntegerField(default=0)
    

class Food(models.Model):
    food_id = models.BigAutoField(primary_key=True)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name='foods')
    food_name = models.CharField(max_length=100)
    food_type = models.CharField(max_length=100)
    food_calorie = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    recipe = models.TextField()
    grain = models.IntegerField(default=0)
    fish_meat_low_fat = models.IntegerField(default=0)
    fish_meat_medium_fat = models.IntegerField(default=0)
    fruit = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    dairy = models.IntegerField(default=0)
    vegetable = models.IntegerField(default=0)

    def __str__(self):
        return self.food_name


class FoodExchangeListCalorie(models.Model):
    food_exchange_list_calorie_id = models.BigAutoField(primary_key=True)
    energy_calorie = models.IntegerField(default=0)
    grain = models.IntegerField(default=0)
    fish_meat_low_fat = models.IntegerField(default=0)
    fish_meat_medium_fat = models.IntegerField(default=0)
    fruit = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    dairy = models.IntegerField(default=0)
    vegetable = models.IntegerField(default=0)

    def __int__(self):
        return self.energy_calorie

class FoodExchangeListProduct(models.Model):
    food_exchange_list_product_id = models.BigAutoField(primary_key=True)
    grain_product = models.CharField(max_length=100)
    fish_meat_low_fat_product = models.TextField()
    fish_meat_medium_fat_product = models.TextField()
    fruit_product = models.TextField()
    fat_product = models.TextField()
    dairy_product = models.TextField()
    vegetable_product = models.TextField()