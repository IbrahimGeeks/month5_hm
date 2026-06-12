import random
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserConfirmation

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False 
        )
        
        random_code = str(random.randint(100000, 999999))
        
        UserConfirmation.objects.create(user=user, code=random_code)
        
        print(f"\n========================================")
        print(f"КОД ПОДТВЕРЖДЕНИЯ ДЛЯ {user.username}: {random_code}")
        print(f"========================================\n")
        
        return user



class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)