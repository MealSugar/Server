from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404

class DietDetailView(APIView):
    def get(self, request, pk):
        diet = get_object_or_404(Diet, pk=pk)
        if diet.is_my_recipe or diet.user == request.user:
            data = {
                "nickname": diet.user.nickname,
                "date": diet.created_at,
                "meal_time": diet.meal_time,
                "meal_type": diet.meal_type,
                "is_my_recipe": diet.is_my_recipe,
                "calorie": diet.diet_calorie,
                "heart": diet.heart_count,
            }

            foods = Food.objects.filter(diet=diet)
            
            for food in foods:
                food_data = {
                    "food_name": food.food_name,
                    "nutrients": {
                        "grain": food.grain,
                        "fish_meat_low_fat": food.fish_meat_low_fat,
                        "fish_meat_medium_fat": food.fish_meat_medium_fat,
                        "vegetable": food.vegetable,
                        "fat": food.fat,
                        "dairy": food.dairy,
                        "fruit": food.fruit
                    },
                    "recipe": food.recipe
                }

                data[food.food_type] = food_data

            if diet.diet_img:
                data["image"] = diet.diet_img
                
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "access denied."}, status=status.HTTP_403_FORBIDDEN)
