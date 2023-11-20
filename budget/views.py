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
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date is None or end_date is None:
            return Response({"message" : "기간을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        result = []
        input_data = {
            "user" : user.id,
            "start_date" : start_date,
            "end_date" : end_date
        }
        budget_data = request.data.get('budget_data')
        for category, money in budget_data.items():
            try:
                category_id = Category.objects.get(name=category).id
            except:
                return Response({"message" : f"{category} : 해당 카테고리는 사용할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

            input_data['category'] = category_id
            input_data['money'] = money

            serializer = BudgetSerializer(data=input_data)
            serializer.is_valid(raise_exception=True)
            saved_data = serializer.save()
            output_data = BudgetDetailSerializer(saved_data).data
            result.append(output_data)

        return Response(result, status=status.HTTP_201_CREATED)
        

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
    

    def delete(self, request, budget_id):
        user = request.user

        try:
            budget = Budget.objects.get(id=budget_id, user=user)
        except Exception as e:
            return Response({"error_message" : str(e), "message" : "해당 예산 정보를 삭제할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        budget.delete()

        return Response({"message" : "예산 정보가 삭제되었습니다."}, status=status.HTTP_200_OK)





