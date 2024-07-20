from django.db import models
from accounts.models import User

class Food(models.Model):
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    food_type = models.CharField(max_length=100)
    food_calorie = models.IntegerField(blank=True, null=True)
    food_date = models.DateTimeField(auto_now_add=True)
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

class Diet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet_set = models.ForeignKey(DietSet, on_delete=models.CASCADE)
    diet_name = models.CharField(max_length=100)
    diet_calorie = models.IntegerField(blank=True, null=True)
    diet_date = models.DateField(auto_now_add=True, blank=True, null=True)
    diet_img = models.ImageField(upload_to='diet_photos/', blank=True, null=True)
    meal_time = models.CharField(max_length=100, blank=True, null=True)
    meal_type = models.CharField(max_length=100, blank=True, null=True)
    is_my_recipe = models.BooleanField(default=False)
    is_like = models.BooleanField(default=False)
    heart_count = models.IntegerField(default=0)

    def __str__(self):
        return self.diet_name

class FoodExchangeListCalorie(models.Model):
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
    grain_product = models.CharField(max_length=100)
    fish_meat_low_fat_product = models.TextField()
    fish_meat_medium_fat_product = models.TextField()
    fruit_product = models.TextField()
    fat_product = models.TextField()
    dairy_product = models.TextField()
    vegetable_product = models.TextField()

class DietSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
