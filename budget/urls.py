from django.urls import path

from budget.views import BudgetAPIView

urlpatterns = [
    path('', BudgetAPIView.as_view()),
]