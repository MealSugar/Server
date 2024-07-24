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