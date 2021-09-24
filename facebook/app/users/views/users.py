"""Users views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Models
from app.users.models import User
from app.users.permissions import IsAccountOwner

# Serializers
from app.users.serializers import (AccountVerificationSerializer,
                                   RefreshTokenSerializer,
                                   RestorePasswordSerializer,
                                   TokenRestorePasswordSerializer,
                                   UpdatePasswordSerializer,
                                   UserLoginSerializer, UserModelSerializer,
                                   UserSignUpSerializer)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    User view set.
    Handle signup, login and account verification,
    refresh token, restore and update password.
    """

    queryset = User.objects.filter(is_verified=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            'signup', 'login', 'verify', 'refresh_token', 
            'token_restore_password', 'restore_password']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
           permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data, 'access_token': token}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations, you can now start using Facebook and connecting with friends.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """Refresh a token verification."""
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'We send you an new account verification message to your email.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def token_restore_password(self, request):
        """Create a token for restore password."""
        serializer = TokenRestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'We have sent an email for you to reset your password.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def restore_password(self, request):
        """Restore user's password."""
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Your password has been reset.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_password(self, request, *args, **kwargs):
        """Update user's password."""
        serializer = UpdatePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
