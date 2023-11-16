from django.urls import path

from expenditure.views import ExpenditureAPIView, ExpenditureDetailAPIView

urlpatterns = [
    path('', ExpenditureAPIView.as_view()),
    path('<int:expenditure_id>/', ExpenditureDetailAPIView.as_view()),
]