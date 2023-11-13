from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from users.serializers import SignupOutputSerializer, SignupSerializer


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


    
