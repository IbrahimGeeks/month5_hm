from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import UserConfirmation
from .serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer

@api_view(['POST'])
def register_api_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            data={'message': 'Пользователь создан! отправьте код подтверждения.'}, 
            status=status.HTTP_201_CREATED
        )
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        code = serializer.validated_data['code']
        
        try:
            confirmation = UserConfirmation.objects.get(user__username=username, code=code)
            
            user = confirmation.user
            user.is_active = True
            user.save()
            confirmation.delete()
            
            return Response(data={'message': 'Аккаунт успешно активирован! Теперь вы можете войти.'}, status=status.HTTP_200_OK)
            
        except UserConfirmation.DoesNotExist:
            return Response(data={'error': 'Неверное имя пользователя или код подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)
            
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_api_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                data={'error': 'Неверные учетные данные или аккаунт еще не активирован.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)