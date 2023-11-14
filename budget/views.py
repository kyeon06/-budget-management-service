from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from budget.models import Budget
from budget.serializers import BudgetCreateSerializer, BudgetListSerializer, BudgetSerializer
from categories.models import Category


# api/v1/budget/
class BudgetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        예산 목록
        """
        user = request.user

        budget_list = Budget.objects.filter(user=user)
        
        serializer = BudgetListSerializer(budget_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=BudgetCreateSerializer,
                         responses={status.HTTP_201_CREATED : BudgetListSerializer})
    def post(self, request):
        """
        예산 생성
        """
        user = request.user
        budget_data = request.data

        required_field = (not budget_data['money']) or (not budget_data['start_date']) or (not budget_data['end_date'])
        if required_field:
            raise ValueError("예산 기간과 금액을 입력해주세요.")
        
        category = budget_data['category']
        if category:
            budget_data['category'] = Category.objects.get(name=category).id
        
        budget_data["user"] = user.id

        serializer = BudgetSerializer(data=budget_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        







