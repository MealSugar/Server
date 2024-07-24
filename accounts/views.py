from django.shortcuts import render, get_object_or_404

from diets.models import FoodExchangeListCalorie

from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
# from django.contrib.auth.models import AnonymousUser


class RefreshAPIView(APIView):
    permission_classes = [AllowAny]
    # access token 재발급
    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"message": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh_token = RefreshToken(refresh)
            access_token = str(refresh_token.access_token)
        except TokenError as e:
            return Response({"message": f"Invalid token: {e}"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"access_token": access_token}, status=status.HTTP_200_OK)


class JoinAPIView(APIView):
    permission_classes = [AllowAny]
    # 회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            res = Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_200_OK)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IdCheckAPIView(APIView):
    permission_classes = [AllowAny]
    # 아이디 중복 체크
    def post(self, request):
        id = request.data.get("id")
        if not id:
            return Response({"message": "ID를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
        try: 
            get_object_or_404(User, id=id)
            return Response({"message": "해당 ID는 사용할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "사용할 수 있는 아이디입니다."}, status=status.HTTP_200_OK)
    
class NicknameCheckAPIView(APIView):
    permission_classes = [AllowAny]
    # 닉네임 중복 체크
    def post(self, request):
        nickname = request.data.get("nickname")
        if not nickname:
            return Response({"message": "닉네임을 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
        try: 
            get_object_or_404(User, nickname=nickname)
            return Response({"message": "해당 닉네임은 사용할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "사용할 수 있는 닉네임입니다."}, status=status.HTTP_200_OK)
        
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    # 로그인
    def post(self, request):
        # 유저 인증
        user = authenticate(
            id=request.data.get("id"), password=request.data.get("password")
        )
        # 아이디, 비번이 맞았을 때
        if user is not None:
            try:
                refresh = request.COOKIES.get('refresh')
                if refresh:
                    refresh_token = RefreshToken(refresh)
                    refresh_token.blacklist()
            except TokenError as e:
                pass

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "message": "login success",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
                status=status.HTTP_200_OK,
            )
            return res
        else: # id나 비번 둘 중 하나가 틀렸을 때
            return Response({"message": "Login failed"}, status=status.HTTP_400_BAD_REQUEST)
        
class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 내 정보 수정 및 진단테스트
    def patch(self, request):
        user = request.user
        serializer = UserInfoSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            temp = (float(user.height) / 100) **2
            if user.gender == '남성':
                temp *= 22
            else:
                temp *= 21
            daily_cal = ((int(temp) * 30)//100)*100
            try:
                food_exchange = FoodExchangeListCalorie.objects.get(energy_calorie=daily_cal)
                user.food_exchange_list_calorie = food_exchange
            except:
                user.food_exchange_list_calorie = None
            user.save()
            return Response({"message": "data save success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class FoodExchangeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 식품교환표 전달
    def get(self, request):
        user = request.user
        try:
            food_exchange = user.food_exchange_list_calorie
            if not food_exchange:
                return Response({"message": "There is no match food_exchange"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = FoodExchangeSerializer(food_exchange)
            res = {
            "nickname": user.nickname,
            "food_exchange": serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response({"message": "There is no match food_exchange"}, status=status.HTTP_400_BAD_REQUEST)