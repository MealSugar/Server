from django.db import models
from django.conf import settings

class BloodSugarState(models.Model):
    blood_sugar_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='BloodSugarStates')
    morning_fasting_blood_sugar = models.IntegerField(verbose_name="아침 공복 혈당", null=True, blank=True)
    noon_fasting_blood_sugar = models.IntegerField(verbose_name="점심 공복 혈당", null=True, blank=True)
    evening_fasting_blood_sugar = models.IntegerField(verbose_name="저녁 공복 혈당", null=True, blank=True)
    morning_post_meal_blood_sugar = models.IntegerField(verbose_name="아침 식후 2시간 이후 혈당", null=True, blank=True)
    noon_post_meal_blood_sugar = models.IntegerField(verbose_name="점심 식후 2시간 이후 혈당", null=True, blank=True)
    evening_post_meal_blood_sugar = models.IntegerField(verbose_name="저녁 식후 2시간 이후 혈당", null=True, blank=True)
    created_at = models.DateField(verbose_name="작성일", auto_now_add=True)
    #해당 날짜와 유저 id 값 일치하는 object가 있는지 확인하고 없으면 만들고 있으면 새로 만들지 말고 값만 바꿔서 save

class TargetBloodSugar(models.Model):
    target_blood_sugar_id = models.BigAutoField(primary_key=True)
    height = models.IntegerField(verbose_name="키", default=0)
    weight = models.IntegerField(verbose_name="몸무게", default=0)
    max_age = models.IntegerField(default=0)
    min_age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, blank=True)
    target_blood_sugar = models.IntegerField(verbose_name="목표 혈당 수치", default=0)