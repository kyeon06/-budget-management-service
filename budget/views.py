from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from budget.models import Budget
from budget.serializers import BudgetCreateSerializer, BudgetDetailSerializer, BudgetListSerializer, BudgetSerializer, BudgetUpdateSerializer
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
    
    
    @swagger_auto_schema(
            request_body=BudgetCreateSerializer,
            responses={
                status.HTTP_201_CREATED : BudgetListSerializer
            }
    )
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
        

# api/v1/budget/<int:budget_id>/
class BudgetDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, budget_id):
        user = request.user

        try:
            budget = Budget.objects.get(id=budget_id, user=user)
            serializer = BudgetDetailSerializer(budget)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error_message" : str(e), "message" : "해당 예산 정보를 확인할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
            request_body=BudgetUpdateSerializer,
            responses={
                status.HTTP_200_OK : BudgetDetailSerializer
            }
    )
    def put(self, request, budget_id):
        user = request.user

        try:
            budget = Budget.objects.get(id=budget_id, user=user)
        except Exception as e:
            return Response({"error_message" : str(e), "message" : "해당 예산 정보를 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            updated_budget = serializer.save()
            return Response(BudgetDetailSerializer(updated_budget).data, status=status.HTTP_200_OK)

        return Response({"message" : "예산 수정을 실패했습니다. 다시 시도해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        






