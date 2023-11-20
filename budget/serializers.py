from rest_framework import serializers

from budget.models import Budget


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = [
            'id',
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
            'id',
            'user',
            'category',
            'money',
            'start_date',
            'end_date'
        ]


class BudgetCreateSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    budget_data = serializers.DictField()


class BudgetDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    
    class Meta:
        model = Budget
        fields = [
            'id',
            'category',
            'money',
            'start_date',
            'end_date',
            'created_at',
            'updated_at'
        ]


class BudgetUpdateSerializer(serializers.Serializer):
    category = serializers.CharField()
    money = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()