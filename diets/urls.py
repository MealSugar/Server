from django.urls import path, include
from .views import *

urlpatterns = [
    path('detail/<int:pk>/', DietDetailView.as_view()),
]