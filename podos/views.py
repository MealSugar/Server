from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from accounts.models import User
# Create your views here.

class StoreAPIView(APIView):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        podo = PodoStore.objects.all()

        data = {
            "nickname": user.nickname,
            "remained_podo": user.remained_podo,
            "items" : StoreSerializer(podo, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

class ExchangeAPIView(APIView):
    def post(self, request, id):
        podo_store = get_object_or_404(PodoStore, podo_store_id=id)

        user = request.user
        remaining_podo = user.remained_podo - podo_store.price

        if remaining_podo < 0:
            return Response({"error": "Not enough remaining podo"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['podo_store'] = podo_store.podo_store_id
        request.data['remaining_points'] = remaining_podo

        serializer = HistorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            user.remained_podo = remaining_podo
            user.used_podo += podo_store.price
            user.save()
            return Response({
                "message": "Podo history data saved successfully.",
                "remained_podo": user.remained_podo
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryAPIView(APIView):
    def get(self, request):
        user = request.user
        podo = PodoHistory.objects.filter(user = request.user, podo_store__isnull = False)
        point = PodoHistory.objects.filter(user = request.user, podo_point_list__isnull=False)

        purchased_data = [
            {
                "date": data.created_at,
                "items": data.podo_store.item_name,
                "item_price": data.podo_store.price,
                "remaining_points": data.remaining_points
            }
            for data in podo
        ]
        
        received_data = [
            {
                "date": data.created_at,
                "items": data.podo_point_list.item_name,
                "received_points": data.podo_point_list.points,
                "remaining_points": data.remaining_points
            }
            for data in point
        ]

        data = {
            "cumulative_podo": user.cumulative_podo,
            "used_podo": user.used_podo,
            "remained_podo": user.remained_podo,
            "purchased_list": purchased_data,
            "received_list": received_data
        }
        return Response(data, status=status.HTTP_200_OK)