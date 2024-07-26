from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('join/', JoinAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('id-check/', IdCheckAPIView.as_view()),
    path('nickname-check/', NicknameCheckAPIView.as_view()),
    path('refresh/', RefreshAPIView.as_view()),
    path('diagnosis/', UserAPIView.as_view()),
    path('mypage/myinfo/edit/', UserAPIView.as_view()),
    path('food-exchange-list/', FoodExchangeAPIView.as_view()),
    path('mypage/myinfo/', UserAPIView.as_view()),
    path('mypage/', MypageAPIView.as_view()),
    path('mypage/recommended-diet-list/', LikedDietAPIView.as_view()),
]