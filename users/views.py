from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken 

from .models import UserConfirmation
from .serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer

class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'message': 'Пользователь создан! отправьте код подтверждения.'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAPIView(APIView):
    serializer_class = ConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            try:
                confirmation = UserConfirmation.objects.get(user__email=email, code=code)
                user = confirmation.user
                user.is_active = True
                user.save()
                confirmation.delete()
                
                return Response(
                    data={'message': 'Аккаунт успешно активирован! Теперь вы можете войти.'}, 
                    status=status.HTTP_200_OK
                )
            except UserConfirmation.DoesNotExist:
                return Response(
                    data={'error': 'Неверный email или код подтверждения.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response(
                data={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, 
                status=status.HTTP_200_OK
            )
            
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)