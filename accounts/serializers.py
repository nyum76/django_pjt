from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname']


    def validate_username(self, value):
        # 사용자 이름 중복 체크
        if User.objects.filter(username=value).exists():
            raise ValidationError("이미 가입된 사용자입니다.")
        return value

    def create(self, validated_data):
        # 비밀번호는 암호화해서 저장
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data.get('nickname')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
