from rest_framework import serializers

from budget.models import Budget


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = [
            'user',
            'category',
            'money',
            'start_date',
            'end_date'
        ]


class BudgetListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Budget
        fields = [
            'user',
            'category',
            'money',
            'start_date',
            'end_date'
        ]


class BudgetCreateSerializer(serializers.Serializer):
    category = serializers.CharField()
    money = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()