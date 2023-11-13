from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate

from users.serializers import LoginSerializer, SignupOutputSerializer, SignupSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# api/v1/users/signup/
class SignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses = {
            status.HTTP_201_CREATED : SignupOutputSerializer
        }
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            data = {
                "username" : user.username,
                "message" : "회원가입이 완료되었습니다."
            }

            return Response(data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/v1/users/login/
class LoginView(APIView):
    
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            raise ValueError("username, password를 입력해주세요.")
        
        user = authenticate(username=username, password=password)

        if user:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            data = {
                "message" : "로그인 완료",
                "username" : user.get_username(),
                "token" : {
                    "refresh_token" : refresh_token,
                    "access_token" : access_token,
                }
            }

            return Response(data, status=status.HTTP_200_OK)
        
        return Response({"message":"로그인 실패, 다시 시도해주세요."}, status=status.HTTP_404_NOT_FOUND)


# api/v1/users/logout/
class LogoutView(APIView):
    pass