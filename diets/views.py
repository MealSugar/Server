from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import timedelta
from django.utils import timezone

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
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        weekly_diets = Diet.objects.filter(created_at__range=(start_of_week.date(), end_of_week.date()))
        sorted_diets = weekly_diets.order_by('-heart_count', 'user__created_at', '-diet_id')

        data = {
            "first_nickname": sorted_diets[0].user.nickname if len(sorted_diets)>0 else "",
            "second_nickname": sorted_diets[1].user.nickname if len(sorted_diets)>1 else "",
            "third_nickname": sorted_diets[2].user.nickname if len(sorted_diets)>2 else "",
            "diets": []
        }

        if len(sorted_diets)>0:
            for diet in sorted_diets:
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
                    "main": main if main else "",
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


class DietLikeView(APIView):
    def patch(self, request, pk):
        diet_set = get_object_or_404(DietSet, pk=pk)
        diet = get_list_or_404(Diet, diet_set=diet_set)
        serializer = DietLikeSerializer(diet, data=request.data, partial=True)
        
        if serializer.is_valid():
            is_like = serializer.validated_data['is_like']
            serializer.save()
            if is_like:
                return Response({"message": "like success"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "like cancel"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DietRegisterView(APIView):
    def post(self, request):
        main_data = request.data.get('main', {})
        side1_data = request.data.get('side1', {})
        side2_data = request.data.get('side2', {})
        side3_data = request.data.get('side3', {})

        main_data['food_type'] = 'main' if main_data else None
        side1_data['food_type'] = 'side1' if side1_data else None
        side2_data['food_type'] = 'side2' if side2_data else None
        side3_data['food_type'] = 'side3' if side3_data else None

        def pop_nutrients(data):
            food_data = data.pop('nutrients', {})
            combined_data = {**food_data, **data}
            return combined_data

        main_food_data = pop_nutrients(main_data)
        side1_food_data = pop_nutrients(side1_data)
        side2_food_data = pop_nutrients(side2_data)
        side3_food_data = pop_nutrients(side3_data)

        user = request.user
        diet = Diet.objects.create(user=user, is_my_recipe=True)

        for food_data in [main_food_data, side1_food_data, side2_food_data, side3_food_data]:
            if food_data['food_type']:
                serializer = MyFoodRegisterSerializer(data=food_data)
                if serializer.is_valid():
                    serializer.save(diet=diet)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "register success."}, status=status.HTTP_201_CREATED)
