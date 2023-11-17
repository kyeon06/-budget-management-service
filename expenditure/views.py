from django.db.models import Q, Sum, F

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from categories.models import Category
from expenditure.models import Expenditure
from expenditure.serializers import ExpenditureCreateSerializer, ExpenditureDetailSerializer, ExpenditureListSerializer, ExpenditureSerializer


# api/v1/expenditure/
class ExpenditureAPIView(APIView):
    """
    지출 내역을 생성하고, 조회하는 기능 관련 API
    """
    permission_classes = [IsAuthenticated]

    query_start_date = openapi.Parameter(
        "start_date",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description="기간(시작)"
    )
    query_end_date = openapi.Parameter(
        "end_date",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description="기간(끝)"
    )
    query_category = openapi.Parameter(
        "category", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="검색 카테고리"
    )
    query_min_m = openapi.Parameter(
        "min_m", openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="검색 최소금액"
    )
    query_max_m = openapi.Parameter(
        "max_m", openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="검색 최대금액"
    )
    @swagger_auto_schema(
        request_body=None,
        responses={
            status.HTTP_200_OK : ExpenditureListSerializer,
        },
        operation_id="지출 목록 조회",
        operation_description="검색/정렬 기준에 대한 지출 목록을 조회합니다.",
        manual_parameters=[
            query_start_date,
            query_end_date,
            query_category,
            query_min_m,
            query_max_m
        ]
    )
    def get(self, request):
        query = Q()
        
        user = request.user
        start_date = request.query_params.get('start_date', "2023-11-01")
        end_date = request.query_params.get('end_date', "2023-11-30")
        
        if start_date is None or end_date is None:
            return Response({"message" : "조회 기간을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        category_name = request.query_params.get('category', None)
        min_m = request.query_params.get('min_m', None)
        max_m = request.query_params.get('max_m', None)

        if category_name is not None:
            try:
                category_instance = Category.objects.get(name=category_name)
                query &= Q(category=category_instance)
            except:
                return Response({"message" : "해당 카테고리의 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if min_m is not None and max_m is not None:
            query &= Q(money__range=[min_m, max_m])
        
        query &= Q(user=user)
        query &= Q(expense_date__range=[start_date, end_date])
        query &= Q(is_sum=True)

        user_expenditure = Expenditure.objects.filter(query)
        if user_expenditure.exists():
            total_sum = user_expenditure.aggregate(Sum('money')).values()
            sum_category_group = user_expenditure.values('category').annotate(Sum('money')).order_by('category')
            serializer = ExpenditureListSerializer(user_expenditure, many=True)

            result = {
                "expense_list" : serializer.data,
                "sum_category" : sum_category_group,
                "total_sum" : total_sum
            }

            return Response(result, status=status.HTTP_200_OK)
        
        return Response({"message" : "지출 내역이 존재하지 않습니다. 지출을 등록해주세요."}, status=status.HTTP_404_NOT_FOUND)
    

    @swagger_auto_schema(
            request_body=ExpenditureCreateSerializer,
            responses={
                status.HTTP_201_CREATED : ExpenditureDetailSerializer
            }
    )
    def post(self, request):
        """
        money : integer
        comment : text
        category : char
        expense_date : date
        is_sum : boolean
        """
        user = request.user
        input_category = request.data.get('category')

        expense_data = request.data
        required_field = (not expense_data['money']) or (not expense_data['category']) or (not expense_data['expense_date'])
        
        if required_field:
            raise ValueError("지출 금액, 지출일, 지출 카테고리는 필수 입력사항입니다. 다시 입력해주세요.")
        
        try:
            category = Category.objects.get(name=input_category)
        except Exception as e:
            return Response(
                {
                    "error_code" : str(e),
                    "message" : "해당 내역을 찾을 수 없습니다."
                },
                status= status.HTTP_404_NOT_FOUND
                )
        
        expense_data['category'] = category.id
        expense_data['user'] = user.id

        serializer = ExpenditureSerializer(data=expense_data)
        if serializer.is_valid():
            save_data = serializer.save()
            return Response(ExpenditureDetailSerializer(save_data).data, status=status.HTTP_201_CREATED)
        
        return Response({"message" : "지출 생성에 실패하였습니다. 다시 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)


# api/v1/expenditure/<int:expenditure_id>/
class ExpenditureDetailAPIView(APIView):
    """
    지출 내역을 상세 조회하고, 수정, 삭제하는 기능 관련 API
    """
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
            request_body=None,
            responses={
                status.HTTP_200_OK : ExpenditureDetailSerializer
            }
    )
    def get(self, request, expenditure_id):
        user = request.user

        try:
            expense_data = Expenditure.objects.get(user=user, id=expenditure_id)
        except Exception as e :
            return Response(
                {
                    "error_code" : str(e),
                    "message" : "해당 내역을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = ExpenditureDetailSerializer(expense_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
            request_body=ExpenditureCreateSerializer,
            responses={
                status.HTTP_200_OK : ExpenditureDetailSerializer
            }
    )
    def put(self, request, expenditure_id):
        user = request.user
        update_data = request.data

        try:
            expense_data = Expenditure.objects.get(user=user, id=expenditure_id)
            category_data = Category.objects.get(name=update_data['category'])
        except Exception as e :
            return Response(
                {
                    "error_code" : str(e),
                    "message" : "해당 내역을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
                )
        
        update_data['category'] = category_data.id

        serializer = ExpenditureSerializer(expense_data, data=update_data, partial=True)
        if serializer.is_valid():
            updated_data = serializer.save()
            return Response(ExpenditureDetailSerializer(updated_data).data, status=status.HTTP_200_OK)
        
        return Response({"message" : "내역 수정에 실패하였습니다. 다시 시도해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
            request_body=None
    )
    def delete(self, request, expenditure_id):
        user = request.user

        try:
            data = Expenditure.objects.get(user=user, id=expenditure_id)
        except Exception as e :
            return Response(
                {
                    "error_code" : str(e),
                    "message" : "해당 내역을 찾을 수 없습니다."
                },
                status=status.HTTP_404_NOT_FOUND
                )
        
        data.delete()

        return Response({"message" : "삭제 완료!"}, status=status.HTTP_200_OK)