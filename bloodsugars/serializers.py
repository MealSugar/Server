from rest_framework import serializers
from .models import BloodSugarState

class BloodSugarStateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(write_only=True)
    fasting_blood_sugar = serializers.DictField(child=serializers.IntegerField(allow_null=True), write_only=True)
    post_meal_blood_sugar = serializers.DictField(child=serializers.IntegerField(allow_null=True), write_only=True)

    class Meta:
        model = BloodSugarState
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        date = validated_data['date']
        fasting_blood_sugar = validated_data['fasting_blood_sugar']
        post_meal_blood_sugar = validated_data.pop['post_meal_blood_sugar']

        blood_sugar_state = BloodSugarState.objects.filter(user=user, created_at=date).first()

        if blood_sugar_state:
            blood_sugar_state.morning_fasting_blood_sugar = fasting_blood_sugar.get('morning')
            blood_sugar_state.noon_fasting_blood_sugar = fasting_blood_sugar.get('noon')
            blood_sugar_state.evening_fasting_blood_sugar = fasting_blood_sugar.get('evening')
            blood_sugar_state.morning_post_meal_blood_sugar = post_meal_blood_sugar.get('morning')
            blood_sugar_state.noon_post_meal_blood_sugar = post_meal_blood_sugar.get('noon')
            blood_sugar_state.evening_post_meal_blood_sugar = post_meal_blood_sugar.get('evening')

            blood_sugar_state.save()
        else:
            blood_sugar_state = BloodSugarState.objects.create(
                user=user,
                created_at=date,
                morning_fasting_blood_sugar=fasting_blood_sugar.get('morning'),
                noon_fasting_blood_sugar=fasting_blood_sugar.get('noon'),
                evening_fasting_blood_sugar=fasting_blood_sugar.get('evening'),
                morning_post_meal_blood_sugar=post_meal_blood_sugar.get('morning'),
                noon_post_meal_blood_sugar=post_meal_blood_sugar.get('noon'),
                evening_post_meal_blood_sugar=post_meal_blood_sugar.get('evening')
            )

        return blood_sugar_state



class DailyBloodSugarSerializer(serializers.Serializer):
    date = serializers.DateField()
    fasting_blood_sugar = serializers.DictField(child=serializers.IntegerField(allow_null=True))
    post_meal_blood_sugar = serializers.DictField(child=serializers.IntegerField(allow_null=True))

class WeeklyBloodSugarSerializer(serializers.Serializer):
    date = serializers.DateField()
    fasting_blood_sugar = serializers.IntegerField()
    post_meal_blood_sugar = serializers.IntegerField()

class NormalRangePercentageSerializer(serializers.Serializer):
    low_blood_sugar = serializers.IntegerField()
    caution_low_blood_sugar = serializers.IntegerField()
    normal = serializers.IntegerField()
    caution_high_blood_sugar = serializers.IntegerField()
    high_blood_sugar = serializers.IntegerField()