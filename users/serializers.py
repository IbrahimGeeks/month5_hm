import random
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import UserConfirmation, CustomUser

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        phone_number = validated_data.get('phone_number', None)

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            is_active=False 
        )
        
        random_code = str(random.randint(100000, 999999))
        UserConfirmation.objects.create(user=user, code=random_code)
        
        print(f"\n========================================")
        print(f"КОД ПОДТВЕРЖДЕНИЯ ДЛЯ {user.email}: {random_code}")
        print(f"========================================\n")
        
        return user


class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise ValidationError("Необходимо заполнить оба поля.")

        user = authenticate(email=email, password=password)
        if not user:
            raise ValidationError("Неверный email или password.")

        if not user.is_active:
            raise ValidationError("Пользователь не активирован. Подтвердите email.")

        attrs['user'] = user
        return attrs