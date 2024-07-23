from .models import User
from rest_framework import serializers

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

