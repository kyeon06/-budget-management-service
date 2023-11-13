from django.urls import path

from categories.views import CategoryAPIView

urlpatterns = [
    path('', CategoryAPIView.as_view(), name='category-list'),
]