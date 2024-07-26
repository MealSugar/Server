from rest_framework import serializers
from .models import *

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodoStore
        fields = '__all__'

class PointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodoPointList
        fields = '__all__'
 
class HistorySerializer(serializers.ModelSerializer):
    podo_store = serializers.PrimaryKeyRelatedField(queryset=PodoStore.objects.all())
    podo_point_list = serializers.PrimaryKeyRelatedField(queryset=PodoPointList.objects.all(), allow_null=True, required=False)
    remaining_points = serializers.IntegerField()

    class Meta:
        model = PodoHistory
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        podo_store = validated_data['podo_store']
        podo_point_list = validated_data.pop('podo_point_list', None)
        remaining_points = validated_data['remaining_points']

        podo_history = PodoHistory.objects.create(
            podo_store=podo_store,
            user=user,
            podo_point_list=podo_point_list,
            remaining_points=remaining_points
        )
        return podo_history