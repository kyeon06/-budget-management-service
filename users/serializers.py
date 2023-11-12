from rest_framework import serializers
from users.models import User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("유저가 존재합니다. 다른 계정명을 사용해주세요.")
        
        user = User.objects.create_user(username=username, password=password)

        return user

class SignupOutputSerializer(serializers.Serializer):
    username = serializers.CharField()
    message = serializers.CharField()