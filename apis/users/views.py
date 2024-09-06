from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserUpdateSerializer, PasswordChangeSerializer
from django.contrib.auth.models import User


class CreateUserView(CreateAPIView):
    """
    Create a new user
    """
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeactivateUserView(APIView):
    """
    Deactivate a user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user

        user.is_active = False
        user.save()

        return Response({"detail": "Account Deactivated"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    Change password of a user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    """
    Update user's username
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        ser_data = UserUpdateSerializer(data=request.data)
        if ser_data.is_valid():
            user = request.user
            user.username = ser_data.data['username']
            user.save()
            return Response({"detail": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
