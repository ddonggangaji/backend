from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import *

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["user_name", "password", "re_password", "nick_name", "phone_number", "role"]

    def create(self, validated_data):
        if validated_data["password"] != validated_data["re_password"]:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            validated_data.pop("re_password")
            user = User.objects.create(**validated_data)
            return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "user_name", "phone_number", "nick_name", "role"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
