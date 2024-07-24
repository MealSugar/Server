from django.urls import path
from .views import *

urlpatterns = [
    path('save/', BloodSugarAPIView.as_view()),
    path('state/', StateAPIView.as_view()),
]
