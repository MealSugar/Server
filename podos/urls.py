from django.urls import path
from .views import *

urlpatterns = [
    path('store/', StoreAPIView.as_view()),
    path('exchange/<int:id>/', ExchangeAPIView.as_view()),
    path('history/', HistoryAPIView.as_view()),
]