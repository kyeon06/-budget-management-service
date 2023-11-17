from rest_framework import serializers

from expenditure.models import Expenditure


class ExpenditureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenditure
        fields = ('__all__')


class ExpenditureListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Expenditure
        fields = [
            'id',
            'category',
            'money',
            'expense_date'
        ]


class ExpenditureDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Expenditure
        fields = [
            'id',
            'user',
            'category',
            'money',
            'comment',
            'expense_date',
            'is_sum',
            'created_at',
            'updated_at'
        ]


class ExpenditureCreateSerializer(serializers.Serializer):
    money = serializers.IntegerField()
    comment = serializers.CharField()
    category = serializers.CharField()
    expense_date = serializers.DateField(format="%Y-%m-%d")
    is_sum = serializers.BooleanField(default=True)

