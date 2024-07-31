from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from diets.models import FoodExchangeListCalorie

class UserManager(BaseUserManager):
    def create_user(self, id, nickname, password, email, **kwargs):
        user = self.model(
            id=id,
            nickname = nickname,
            password = password,
            email = email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id=None, nickname=None, password=None, email=None, **extra_fields):
        superuser = self.create_user(
            id=id,
            nickname = nickname,
            password = password,
            email = email
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    id = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=2, blank=True)
    age = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    is_diabetes = models.BooleanField(default=False)
    fasting_blood_sugar = models.IntegerField(null=True, blank=True)
    post_meal_blood_sugar = models.IntegerField(null=True, blank=True)
    is_subscribe = models.BooleanField(default=False)
    cumulative_podo = models.IntegerField(default=0)
    used_podo = models.IntegerField(default=0)
    remained_podo = models.IntegerField(default=0)
    recommend_count = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    food_exchange_list_calorie = models.ForeignKey(FoodExchangeListCalorie, on_delete=models.SET_NULL, related_name='user', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['nickname', 'email']

    def __str__(self):
        return self.nickname