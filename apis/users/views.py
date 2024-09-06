from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserUpdateSerializer, PasswordChangeSerializer
from django.contrib.auth.models import User


class CreateUserView(CreateAPIView):
    """
    View to create a new user.

    Allows anyone (authenticated or not) to create a new user account.

    Permissions:
    - AllowAny: No authentication required to create a new user.

    Request body:
    - User data in JSON format, should include fields required by `UserSerializer`.

    Responses:
    - 201: User created successfully.
    - 400: Invalid data provided.
    """
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeactivateUserView(APIView):
    """
    View to deactivate the currently authenticated user.

    Only authenticated users can deactivate their own account.

    Permissions:
    - IsAuthenticated: User must be authenticated to deactivate their account.

    Responses:
    - 200: Account successfully deactivated.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Deactivate the user account.

        The account will be deactivated by setting the `is_active` field to `False`.

        Responses:
        - 200: Account deactivated successfully.
        """
        user = request.user

        user.is_active = False
        user.save()

        return Response({"detail": "Account Deactivated"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    View to change the password of the currently authenticated user.

    Only authenticated users can change their own password.

    Permissions:
    - IsAuthenticated: User must be authenticated to change their password.

    Request body:
    - Old password, new password, and confirmation of the new password in JSON format, validated by `PasswordChangeSerializer`.

    Responses:
    - 200: Password changed successfully.
    - 400: Invalid data or password change failed.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Change the user's password.

        The request data should include the old password and the new password.

        Responses:
        - 200: Password changed successfully.
        - 400: Invalid data or password change failed.
        """
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    """
    View to update the username of the currently authenticated user.

    Only authenticated users can update their own username.

    Permissions:
    - IsAuthenticated: User must be authenticated to update their username.

    Request body:
    - New username in JSON format, validated by `UserUpdateSerializer`.

    Responses:
    - 200: Username updated successfully.
    - 400: Invalid data or update failed.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Update the username of the user.

        The request data should include the new username.

        Responses:
        - 200: Username updated successfully.
        - 400: Invalid data or update failed.
        """
        ser_data = UserUpdateSerializer(data=request.data)
        if ser_data.is_valid():
            user = request.user
            user.username = ser_data.data['username']
            user.save()
            return Response({"detail": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
