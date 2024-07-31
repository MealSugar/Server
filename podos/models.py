from django.db import models
from django.conf import settings

# Create your models here.
class PodoStore(models.Model):
    podo_store_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(verbose_name="상품 이름", max_length=100)
    price = models.IntegerField(verbose_name="가격", default=0)

class PodoPointList(models.Model):
    podo_point_list_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(verbose_name="적립 포인트 항목 이름", max_length=100)
    points = models.IntegerField(verbose_name="포인트", default=0)

class PodoHistory(models.Model):
    podo_history_id = models.BigAutoField(primary_key=True)
    podo_store = models.ForeignKey(PodoStore, on_delete=models.CASCADE, null=True, blank=True, related_name= 'PodoHistories')
    created_at = models.DateField(verbose_name="구매일", auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name= 'PodoHistories')
    remaining_points = models.IntegerField(verbose_name="당시 남은 포인트")
    podo_point_list = models.ForeignKey(PodoPointList, on_delete=models.CASCADE, null=True, blank=True, related_name= 'PodoHistories')
