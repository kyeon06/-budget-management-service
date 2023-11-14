from rest_framework import serializers

from budget.models import Budget


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