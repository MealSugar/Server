from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
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

class DiethonView(APIView):
    def get(self, request):
        top_diets = Diet.objects.order_by('-heart_count', 'user__created_at', '-diet_id')[:3]

        data = {
            "first_nickname": top_diets[0].user.nickname if len(top_diets)>0 else "",
            "second_nickname": top_diets[1].user.nickname if len(top_diets)>1 else "",
            "third_nickname": top_diets[2].user.nickname if len(top_diets)>2 else "",
            "diets": []
        }

        if len(top_diets)>0:
            for diet in top_diets:
                foods = Food.objects.filter(diet=diet)
                main = None
                sides = []

                for food in foods:
                    if food.food_type == 'main':
                        main = food.food_name
                    else:
                        sides.append(food.food_name)

                diet_data = {
                    "diet_id": diet.diet_id,
                    "nickname": diet.user.nickname,
                    "main": main,
                    "side1": sides[0] if len(sides)>0 else "",
                    "side2": sides[1] if len(sides)>1 else "",
                    "side3": sides[2] if len(sides)>2 else ""
                }

                serializer = DiethonSerializer(data=diet_data)
                if serializer.is_valid():
                    data["diets"].append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)


class DietHeartView(APIView):
    def patch(self, request, pk):
        diet = get_object_or_404(Diet, pk=pk)
        serializer = DietHeartSerializer(diet, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "heart changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
