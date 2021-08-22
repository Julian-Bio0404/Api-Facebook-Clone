"""Users views."""

# Django
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST framework
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from users.models import User

# Serializers
from users.serializers import (AccountVerificationSerializer,
                               UpdatePasswordSerializer,
                               UserLoginSerializer, 
                               UserModelSerializer,
                               UserSignUpSerializer,
                               RestorePasswordSerializer)

# Utilities
from datetime import timedelta
import jwt


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.
    Handle signup, login and account verification."""

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'username'

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
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations, you can now start using Facebook and connecting with friends.'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """Refresh a token verification."""
        user = authenticate(
            username=request.data['email'], password=request.data['password'])

        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        else:
            exp_date = timezone.now() + timedelta(days=2)
            payload = {
                'user': user.username,
                'exp': int(exp_date.timestamp()),
                'type': 'email_confirmation'
            }
            # Generacion del token
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            subject = 'Welcome @{}! Verify your account'.format(user.username)
            from_email = 'Facebook <Facebook.com>'
            content = render_to_string(
                'account_verification.html',
                {'token': token, 'user': user}
            )
            msg = EmailMultiAlternatives(
                subject, content, from_email, [user.email])
            msg.attach_alternative(content, 'text/html')
            msg.send()
            data = {
                'message': 'We send you an new account verification message to your email.'
            }
            return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def token_restore_password(self, request):
        """Create a token for restore password."""
        user = User.objects.get(email=request.data['email'])
        exp_date = timezone.now() + timedelta(minutes=20)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'restore_password'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        subject = 'Update your password'
        from_email = 'Facebook <Facebook.com>'
        content = render_to_string(
            'restore_password.html',
            {'token': token, 'user': user})
        msg = EmailMultiAlternatives(
            subject, content, from_email, [user.email])
        msg.attach_alternative(content, 'text/html')
        msg.send()
        data = {
            'message': 'We have sent an email for you to reset your password.'
            }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def restore_password(self, request):
        """Restore user's password."""
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Your password has been reset.'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_password(self, request, *args, **kwargs):
        """Update user's password."""
        serializer = UpdatePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
