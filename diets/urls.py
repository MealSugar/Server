from django.urls import path, include
from .views import *

urlpatterns = [
    path('detail/<int:pk>/', DietDetailView.as_view()),
    path('diethon/', DiethonView.as_view()),
    path('heart/<int:pk>/', DietHeartView.as_view()), 
]