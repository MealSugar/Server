from .models import User
from rest_framework import serializers

from diets.models import FoodExchangeListCalorie

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            
            id = validated_data['id'],
            nickname = validated_data['nickname'],
            password = validated_data['password'],
            email = validated_data['email']
        )
        return user

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'age', 'height', 'weight', 'is_diabetes', 'fasting_blood_sugar', 'post_meal_blood_sugar']


class FoodExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodExchangeListCalorie
        fields = ['energy_calorie', 'grain', 'fish_meat_low_fat', 'fish_meat_medium_fat', 'fruit', 'fat', 'dairy', 'vegetable']
        