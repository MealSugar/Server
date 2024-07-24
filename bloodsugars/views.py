from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BloodSugarState
from .serializers import *

class StateAPIView(APIView):
    def get(self, request):        
        blood_sugar_state = get_object_or_404(BloodSugarState)
        if blood_sugar_state.user == request.user:
            today_data = {
                "date": blood_sugar_state.created_at,
                "fasting_blood_sugar": {
                    "morning": blood_sugar_state.morning_fasting_blood_sugar,
                    "noon": blood_sugar_state.noon_fasting_blood_sugar,
                    "evening": blood_sugar_state.evening_fasting_blood_sugar
                },
                "post_meal_blood_sugar": {
                    "morning": blood_sugar_state.morning_post_meal_blood_sugar,
                    "noon": blood_sugar_state.noon_post_meal_blood_sugar,
                    "evening": blood_sugar_state.evening_post_meal_blood_sugar
                }
            }

            today = timezone.now().date()
            week = today - timedelta(days=6)
            weekly = BloodSugarState.objects.filter(user=request.user, created_at__gte=week, created_at__lte=today)
            weekly_data = []

            for info in weekly:
                fasting_blood_sugar_values = [
                    info.morning_fasting_blood_sugar,
                    info.noon_fasting_blood_sugar,
                    info.evening_fasting_blood_sugar
                ]
                post_blood_sugar_values = [
                    info.morning_post_meal_blood_sugar,
                    info.noon_post_meal_blood_sugar,
                    info.evening_post_meal_blood_sugar
                ]

                count_fasting_blood_sugar_values = [value for value in fasting_blood_sugar_values if value is not None]
                count_post_blood_sugar_values = [value for value in post_blood_sugar_values if value is not None]

                k1 = len(count_fasting_blood_sugar_values)
                k2 = len(count_post_blood_sugar_values)

                avg_fasting_blood_sugar = sum(count_fasting_blood_sugar_values) / k1 if k1 > 0 else None
                avg_post_blood_sugar = sum(count_post_blood_sugar_values) / k2 if k2 > 0 else None

                weekly_data.append({
                    "date": info.created_at,
                    "fasting_blood_sugar": avg_fasting_blood_sugar,
                    "post_meal_blood_sugar": avg_post_blood_sugar
                })

            if request.user.age < 60:
                normal_upper_limit = 140
                caution_lower_limit = 141
            else:
                normal_upper_limit = 160
                caution_lower_limit = 161

            low_blood_sugar_count = sum(1 for data in weekly_data if data["fasting_blood_sugar"] is not None and data["fasting_blood_sugar"] <= 54)
            caution_low_blood_sugar_count = sum(1 for data in weekly_data if data["fasting_blood_sugar"] is not None and 54 < data["fasting_blood_sugar"] < 70)
            normal_count = sum(1 for data in weekly_data if data["fasting_blood_sugar"] is not None and 70 <= data["fasting_blood_sugar"] <= normal_upper_limit)
            caution_high_blood_sugar_count = sum(1 for data in weekly_data if data["fasting_blood_sugar"] is not None and caution_lower_limit < data["fasting_blood_sugar"] <= 199)
            high_blood_sugar_count = sum(1 for data in weekly_data if data["fasting_blood_sugar"] is not None and 200 <= data["fasting_blood_sugar"])

            normal_range_percentage = {
                "low_blood_sugar": low_blood_sugar_count,
                "caution_low_blood_sugar": caution_low_blood_sugar_count,
                "normal": normal_count,
                "caution_high_blood_sugar": caution_high_blood_sugar_count,
                "high_blood_sugar": high_blood_sugar_count
            }

            data = {
                "today_data": DailyBloodSugarSerializer(today_data).data,
                "weekly_data": WeeklyBloodSugarSerializer(weekly_data, many=True).data,
                "normal_range_percentage": NormalRangePercentageSerializer(normal_range_percentage).data
            }

            return Response(data, status=status.HTTP_200_OK)
        
class BloodSugarAPIView(APIView):
    def post(self, request):
        serializer = BloodSugarStateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Blood sugar data saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)