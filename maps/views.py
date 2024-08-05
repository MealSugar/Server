from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Map
from .serializers import *

# Create your views here.

class MapAPIView(APIView):
    def get(self, request):
        cafe = Map.objects.filter(place_type = "cafe")
        restaurant = Map.objects.filter(place_type='restaurant')

        data = {
            "cafe": MapSerializer(cafe, many =True).data,
            "restaurant": MapSerializer(restaurant, many =True).data
        }
        return Response(data, status=status.HTTP_200_OK)
