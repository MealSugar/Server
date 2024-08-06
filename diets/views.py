from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from podos.models import *
from .serializers import *
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import timedelta
from django.utils import timezone
import local_settings
from openai import OpenAI
import ast, json

client = OpenAI(
    api_key=local_settings.API_KEY,
)

def DiethonReward():
    now = timezone.now()
    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    weekly_diets = Diet.objects.filter(created_at__range=(start_of_week.date(), end_of_week.date()))
    sorted_diets = weekly_diets.order_by('-heart_count', 'user__created_at', '-diet_id')
    for i in range(3):
        user = sorted_diets[i].user
        podo_point = PodoPointList.objects.get(item_name = f'식단톤 우승 {i+1}등')
        podohistory = PodoHistory.objects.create(
            user = user,
            remaining_podo = user.remained_podo + podo_point.points,
            podo_point_list = podo_point
        )
        user.cumulative_podo = user.cumulative_podo + podo_point.points
        user.remained_podo = podohistory.remaining_podo
        user.save()

class DietPhoto(APIView):
    def patch(self, request, pk):
        diet = get_object_or_404(Diet, diet_id=pk)
        serializer = DietPhotoSerializer(diet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            diet.is_certificated = True
            return Response({"message": "certificate successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class DietDetailView(APIView):
    def get(self, request, pk):
        diet = get_object_or_404(Diet, pk=pk)
        if diet.is_my_recipe or diet.user == request.user:
            data = {
                "nickname": diet.user.nickname,
                "date": diet.created_at,
                "meal_time": diet.meal_time,
                "meal_type": diet.meal_type,
                "diet_name": diet.diet_name,
                "is_my_recipe": diet.is_my_recipe,
                "heart": diet.heart_count,
            }

            total_food_exchange_list = [0]*7
            total_calorie = 0

            foods = Food.objects.filter(diet=diet)
            
            for food in foods:
                total_food_exchange_list[0] += food.grain
                total_food_exchange_list[1] += food.fish_meat_low_fat
                total_food_exchange_list[2] += food.fish_meat_medium_fat
                total_food_exchange_list[3] += food.vegetable
                total_food_exchange_list[4] += food.fat
                total_food_exchange_list[5] += food.dairy
                total_food_exchange_list[6] += food.fruit

                if food.food_calorie:
                    total_calorie += food.food_calorie

                food_data = {
                    "food_name": food.food_name,
                    "food_calorie": food.food_calorie,
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

            data['total_calorie'] = total_calorie
            data['total_grain'], data['total_fish_meat_low_fat'], data['total_fish_meat_medium_fat'], data['total_vegetable'], data['total_fat'], data['total_dairy'], data['total_fruit'] = total_food_exchange_list[0], total_food_exchange_list[1], total_food_exchange_list[2], total_food_exchange_list[3], total_food_exchange_list[4], total_food_exchange_list[5], total_food_exchange_list[6]


            if diet.diet_img:
                data["image"] = diet.diet_img
                
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "access denied."}, status=status.HTTP_403_FORBIDDEN)

class DiethonView(APIView):
    def get(self, request):
        now = timezone.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        weekly_diets = Diet.objects.filter(is_my_recipe=True, created_at__range=(start_of_week.date(), end_of_week.date()))
        sorted_diets = weekly_diets.order_by('-heart_count', 'user__created_at', '-diet_id')

        data = {
            "first": {
                "first_nickname": sorted_diets[0].user.nickname if len(sorted_diets)>0 else "",
                "diet_name": sorted_diets[0].diet_name if len(sorted_diets)>0 else "",
                "heart": sorted_diets[0].heart_count if len(sorted_diets)>0 else ""
            },
            "second": {
                "second_nickname": sorted_diets[1].user.nickname if len(sorted_diets)>1 else "",
                "diet_name": sorted_diets[1].diet_name if len(sorted_diets)>1 else "",
                "heart": sorted_diets[1].heart_count if len(sorted_diets)>1 else ""
            },
            "third": {
                "third_nickname": sorted_diets[2].user.nickname if len(sorted_diets)>2 else "",
                "diet_name": sorted_diets[2].diet_name if len(sorted_diets)>2 else "",
                "heart": sorted_diets[2].heart_count if len(sorted_diets)>2 else ""
            },
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
                    "diet_name": diet.diet_name,
                    "nickname": diet.user.nickname,
                    "main": main if main else "",
                    "side1": sides[0] if len(sides)>0 else "",
                    "side2": sides[1] if len(sides)>1 else "",
                    "side3": sides[2] if len(sides)>2 else "",
                    "heart": diet.heart_count
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
        diet_name = request.data.get('diet_name', None)
        main_data = json.loads(request.POST.get('main', ''))
        side1_data = json.loads(request.POST.get('side1', ''))
        side2_data = json.loads(request.POST.get('side2', ''))
        side3_data = json.loads(request.POST.get('side3', '')) if request.POST.get('side3', '') else {}
        side4_data = json.loads(request.POST.get('side4', '')) if request.POST.get('side4', '') else {}

        main_data['food_type'] = 'main' if main_data else None
        side1_data['food_type'] = 'side1' if side1_data else None
        side2_data['food_type'] = 'side2' if side2_data else None
        side3_data['food_type'] = 'side3' if side3_data else None
        side4_data['food_type'] = 'side4' if side4_data else None

        def pop_nutrients(data):
            food_data = data.pop('nutrients', {})
            combined_data = {**food_data, **data}
            return combined_data

        main_food_data = pop_nutrients(main_data)
        side1_food_data = pop_nutrients(side1_data)
        side2_food_data = pop_nutrients(side2_data)
        side3_food_data = pop_nutrients(side3_data)
        side4_food_data = pop_nutrients(side4_data)

        user = request.user
        diet_img = request.FILES['image'] if 'image' in request.FILES else None
        diet = Diet.objects.create(diet_name=diet_name, user=user, is_my_recipe=True, diet_img=diet_img)

        for food_data in [main_food_data, side1_food_data, side2_food_data, side3_food_data, side4_food_data]:
            if food_data['food_type']:
                serializer = MyFoodRegisterSerializer(data=food_data)
                if serializer.is_valid():
                    serializer.save(diet=diet)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "register success."}, status=status.HTTP_201_CREATED)


class DietRecommendationView(APIView):
    def post(self, request):
        serializer = DietRecommendationSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            ingredient_list, food_exchange_product_list, combination_list = [], [], ['아침','점심', '저녁']
            output_example = {"breakfast":{"meal_type":"korean","main":{"food_name":"현미밥","grain":2,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":0,"fat":0,"dairy":0,"fruit":0,"food_calorie":200},"side1":{"food_name":"부추겉절이","grain":1,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":1,"fat":0,"dairy":0,"fruit":0,"food_calorie":30},"side2":{"food_name":"계란찜","grain":0,"fish_meat_low_fat":1,"fish_meat_medium_fat":0,"vegetable":0,"fat":1,"dairy":1,"fruit":0,"food_calorie":100},"side3":{"food_name":"미역국","grain":1,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":0,"fat":0,"dairy":0,"fruit":0,"food_calorie":40},"diet_calorie":370},"lunch":{"meal_type":"japanese","main":{"food_name":"두부스테이크","grain":0,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":1,"fat":0,"dairy":0,"fruit":0,"food_calorie":180},"side1":{"food_name":"미소국","grain":1,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":0,"fat":0,"dairy":1,"fruit":0,"food_calorie":70},"side2":{"food_name":"무생채","grain":0,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":1,"fat":0,"dairy":0,"fruit":0,"food_calorie":25},"side3":{"food_name":"브로콜리","grain":0,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":1,"fat":0,"dairy":0,"fruit":0,"food_calorie":20},"diet_calorie":295},"dinner":{"meal_type":"chinese","main":{"food_name":"돼지고기 마늘 볶음","grain":1,"fish_meat_low_fat":0,"fish_meat_medium_fat":2,"vegetable":1,"fat":2,"dairy":0,"fruit":0,"food_calorie":350},"side1":{"food_name":"잡채","grain":1,"fish_meat_low_fat":1,"fish_meat_medium_fat":0,"vegetable":1,"fat":0,"dairy":0,"fruit":0,"food_calorie":200},"side2":{"food_name":"양배추 샐러드","grain":0,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":1,"fat":0,"dairy":0,"fruit":0,"food_calorie":40},"side3":{"food_name":"튀김","grain":1,"fish_meat_low_fat":0,"fish_meat_medium_fat":1,"vegetable":0,"fat":1,"dairy":0,"fruit":0,"food_calorie":200},"diet_calorie":790},"snack1":{"meal_type":"fruit","main":{"food_name":"배(2개)","grain":0,"fish_meat_low_fat":0,"fish_meat_medium_fat":0,"vegetable":0,"fat":0,"dairy":0,"fruit":2,"food_calorie":90},"diet_calorie":90}}
            recipe_example = "닭다리살 또는 닭가슴살: 500g, 밀가루: 1컵, 전분: 1/2컵 (또는 감자전분), 계란: 1개, 식용유: 적당량 (튀김용)"
            
            diet_combination = serializer.validated_data['diet_combination']
            breakfast = serializer.validated_data['breakfast']
            lunch = serializer.validated_data['lunch']
            dinner = serializer.validated_data['dinner']
            ingredient1 = serializer.validated_data.get('ingredient1', None)
            ingredient2 = serializer.validated_data.get('ingredient2', None)
            ingredient3 = serializer.validated_data.get('ingredient3', None)

            if ingredient1:
                ingredient_list.append(ingredient1)
            if ingredient2:
                ingredient_list.append(ingredient2)
            if ingredient3:
                ingredient_list.append(ingredient3)

            if '간식1' in diet_combination:
                combination_list.append('간식1')
            if '간식2' in diet_combination:
                combination_list.append('간식2')

            combination_result = ', '.join(combination_list)

            food_exchange_products = FoodExchangeListProduct.objects.all()
            for product in food_exchange_products:
                food_exchange_product_list.append(f"{product.food_exchange_name}: {product.product}")
            food_exchange_product_example = ', '.join(food_exchange_product_list)

            diet_prompt = f"""
                식단 추천하는데에 가장 중요한 점은 각각의 음식들의 칼로리의 합이 내 하루 권장 칼로리와 정확히 일치해야 하고, 각각의 음식들의 식품군들의 합이 내 하루 식품교환표의 식품군들과 정확히 일치해야 한다는 것이야. 아래 예시처럼 식사들의 식품군 총합이 일치하도록 식단을 추천해줘. 각각의 음식의 식품군들의 합이 내 식품교환표의 식품군과 맞지 않으면 다른 음식을 추천해줘.

                예를 들어:
                - 곡류군: 아침 main 곡류군(1) + 아침 side1 곡류군(0) + 점심 main 곡류군(2) + 저녁 main 곡류군(2) + 간식1 main 곡류군(1) = 내 식품교환표 곡류군(6)
                - 어육류군(저지방군): 아침 main 어육류군(저지방군)(1) + 점심 main 어육류군(저지방군)(0) + 저녁 main 어육류군(저지방군)(1) = 내 식품교환표 어육류군(저지방군)(2)
                - 어육류군(중지방군): 아침 main 어육류군(중지방군)(0) + 점심 main 어육류군(중지방군)(2) + 저녁 main 어육류군(중지방군)(1) = 내 식품교환표 어육류군(중지방군)(3)
                - 과일군: 간식1 main 과일군(1) = 내 식품교환표 과일군(1)
                - 지방군: 아침 main 지방군(1) + 점심 main 지방군(1) + 저녁 main 지방군(1) = 내 식품교환표 지방군(3)
                - 채소군: 아침 main 채소군(2) + 점심 main 채소군(1) + 저녁 main 채소군(1) + 저녁 side1 채소군(2) = 내 식품교환표 채소군(6)
                - 우유군: 간식1 side1 우유군(1) = 내 식품교환표 우유군(1)

                내 하루 권장 칼로리는 {user.food_exchange_list_calorie.energy_calorie} 칼로리야. 내 하루 식단교환표에는 다음과 같은 식품군 교환단위가 있어:
                - 곡류군: {user.food_exchange_list_calorie.grain} 교환단위
                - 어육류군(저지방군): {user.food_exchange_list_calorie.fish_meat_low_fat} 교환단위
                - 어육류군(중지방군): {user.food_exchange_list_calorie.fish_meat_medium_fat} 교환단위
                - 과일군: {user.food_exchange_list_calorie.fruit} 교환단위
                - 지방군: {user.food_exchange_list_calorie.fat} 교환단위
                - 채소군: {user.food_exchange_list_calorie.vegetable} 교환단위
                - 우유군: {user.food_exchange_list_calorie.dairy} 교환단위

                {combination_result}으로 식단을 잘 분배해줘. 각각의 식사의 식품군들의 총합과 칼로리 총합이 내 식품교환표의 식품군과 내 하루 권장 칼로리에 정확히 맞아야 해.

                내가 원하는 출력의 예시: {output_example}, 참고 음식(각각의 음식들은 각 식품군의 1교환단위 기준 예시야): {food_exchange_product_example}.

                해당 예시의 형식에 맞춰서 출력해줘 (예시의 출력 외에 다른 말은 출력하지 말고, '''json도 출력하지 말아줘). 참고 음식들을 참고하여 교환단위에 맞는 적절한 양과 음식을 추천해줘. 내 식사의 조건 - 아침 종류: {breakfast}/ 점심 종류: {lunch}/ 저녁 종류: {dinner}, 들어갔으면 하는 재료: {ingredient_list}이야. main은 무조건 포함시키고 side1, side2, side3는 필수적인 것은 아니야 (diet_calorie, meal_type, food_name, food_calorie, 각종 식품군들은 필수로 출력해줘). 예시와는 다른 {combination_result} 식단을 추천해줘."""


            def chat_gpt(prompt):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "너는 당뇨병 환자들을 위해 특정 조건에 따라 식사를 추천해주는 역할을 갖고 있어. 너한테는 내 하루 권장 칼로리와 내 하루 식품교환표가 주어질거고 출력 예시와 식사 조건 또한 주어질거야."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                return response.choices[0].message.content.strip()

            diet_response = chat_gpt(diet_prompt)
            dictionary_data = ast.literal_eval(diet_response)

            diet_set = DietSet.objects.create(user=user)

            user.recommend_count += 1
            user.save()

            for meal_time in ['breakfast', 'lunch', 'dinner', 'snack1', 'snack2']:
                meal_data = dictionary_data.get(meal_time)
                if meal_data:
                    diet_data = {
                        "user": user.user_id,
                        "diet_set": diet_set.diet_set_id,
                        "diet_calorie": meal_data['diet_calorie'],
                        "meal_time": meal_time,
                        "meal_type": meal_data['meal_type'],
                        "is_my_recipe": False,
                        "is_like": False,
                        "heart_count": 0,
                        "foods": []
                    }

                    for food_type in ['main', 'side1', 'side2']:
                        food_data = meal_data.get(food_type)
                        if food_data:
                            recipe_prompt = f"{food_data['food_name']}의 레시피를 알려줘(요리과정은 알려줄 필요없어). 내가 원하는 출력의 예시: {recipe_example}, 해당 예시의 형식에 맞춰서 출력해줘"
                            recipe_response = chat_gpt(recipe_prompt)

                            diet_data["foods"].append({
                                "food_name": food_data['food_name'],
                                "food_type": food_type,
                                "food_calorie": food_data['food_calorie'],
                                "recipe": recipe_response,
                                "grain": food_data['grain'],
                                "fish_meat_low_fat": food_data['fish_meat_low_fat'],
                                "fish_meat_medium_fat": food_data['fish_meat_medium_fat'],
                                "fruit": food_data['fruit'],
                                "fat": food_data['fat'],
                                "dairy": food_data['dairy'],
                                "vegetable": food_data['vegetable']
                            })

                    diet_serializer = DietRecommendCreateSerializer(data=diet_data)
                    if diet_serializer.is_valid():
                        diet_serializer.save()
                    else:
                        return Response(diet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Diet recommendations created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
