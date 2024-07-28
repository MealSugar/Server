from rest_framework import serializers
from .models import *

class DiethonSerializer(serializers.Serializer):
    diet_id = serializers.IntegerField()
    nickname = serializers.CharField(max_length=20)
    main = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    side1 = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    side2 = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    side3 = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)


class DietHeartSerializer(serializers.ModelSerializer):
    is_heart = serializers.BooleanField()

    class Meta:
        model = Diet
        fields = ['is_heart', 'heart_count']

    def update(self, instance, validated_data):
        is_heart = validated_data.pop('is_heart')
        if is_heart:
            instance.heart_count += 1
        else:
            instance.heart_count -= 1
        instance.save()

        return instance


class DietLikeSerializer(serializers.Serializer):
    is_like = serializers.BooleanField()

    class Meta:
        model = Diet
        fields = ['is_like']

    def update(self, instance, validated_data):
        is_like = validated_data.pop('is_like')
        for instance_diet in instance:
            if is_like:
                instance_diet.is_like = True
            else:
                instance_diet.is_like = False
            instance_diet.save()

        return instance


class MyFoodRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['food_name', 'food_type', 'recipe', 'grain', 'fish_meat_low_fat', 'fish_meat_medium_fat', 'vegetable', 'fat', 'fruit']


class DietRecommendationSerializer(serializers.Serializer):
    diet_combination = serializers.CharField(max_length=15)
    breakfast = serializers.CharField(max_length=15)
    lunch = serializers.CharField(max_length=15)
    dinner = serializers.CharField(max_length=15)
    ingredient1 = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    ingredient2 = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    ingredient3 = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    

class FoodRecommendCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['food_name', 'food_type', 'food_calorie', 'recipe', 'grain', 'fish_meat_low_fat', 'fish_meat_medium_fat', 'fruit', 'fat', 'dairy', 'vegetable']


class DietRecommendCreateSerializer(serializers.ModelSerializer):
    foods = FoodRecommendCreateSerializer(many=True)

    class Meta:
        model = Diet
        fields = ['user', 'diet_set', 'diet_calorie', 'meal_time', 'meal_type', 'is_my_recipe', 'is_like', 'heart_count', 'foods']

    def create(self, validated_data):
        foods_data = validated_data.pop('foods')
        diet = Diet.objects.create(**validated_data)
        for food_data in foods_data:
            Food.objects.create(diet=diet, **food_data)
        return diet