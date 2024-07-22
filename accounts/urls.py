from django.urls import path

from .views import *

from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

# urlpatterns = [
#     path(),
# ]