from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from budget.models import Budget
from budget.serializers import BudgetListSerializer


# api/v1/budget/
class BudgetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        budget_list = Budget.objects.filter(user=user)
        
        serializer = BudgetListSerializer(budget_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        pass


