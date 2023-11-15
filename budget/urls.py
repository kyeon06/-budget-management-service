from django.urls import path

from budget.views import BudgetAPIView, BudgetDetailAPIView

urlpatterns = [
    path('', BudgetAPIView.as_view()),
    path('<int:budget_id>/', BudgetDetailAPIView.as_view()),
]