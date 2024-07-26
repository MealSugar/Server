from django.urls import path
from .views import *

urlpatterns = [
    path('', MapAPIView.as_view()),
]