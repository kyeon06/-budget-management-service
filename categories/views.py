from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from categories.models import Category
from categories.serializers import CategorySerializer

class CategoryAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=None,
        responses={
            status.HTTP_200_OK : CategorySerializer
        }
    )
    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

