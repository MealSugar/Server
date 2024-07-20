from django.db import models
from accounts.models import User

# Create your models here.
class PodoStore(models.Model):
    podo_store_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(verbose_name="상품 이름", max_length=100)
    price = models.IntegerField(verbose_name="가격", default=0)

class PodoUsageHistory(models.Model):
    podo_usage_history_id = models.BigAutoField(primary_key=True)
    podo_store = models.ForeignKey(PodoStore, on_delete=models.CASCADE, null=True, blank=True, related_name= 'PodoUsageHistories')
    created_at = models.DateField(verbose_name="구매일", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= 'PodoUsageHistories')