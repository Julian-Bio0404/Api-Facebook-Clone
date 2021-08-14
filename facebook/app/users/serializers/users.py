"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from users.models import Profile, User, ProfileDetail

# Serializers
from .profiles import ProfileModelSerializer, ProfileModelSummarySerializer

# Utilities
from datetime import timedelta 
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile',
            'is_verified'
        )

        read_only_fields = [
            'profile',
            'is_verified'
        ]

class UserModelSummarySerializer(UserModelSerializer):
    """User model data summary serializer."""

    profile = ProfileModelSummarySerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = User
        fields = [
            'first_name',
            'last_name',
            'profile'
        ]


class UserSignUpSerializer(serializers.Serializer):
    """User signup serializer.
    Handle sign up data validation and user & profile creation."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        min_length=4,
        max_length=25,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    # Phone number
    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.'
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify password match and type identification."""

        # Password
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Password don´t match')
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        ProfileDetail.objects.create(user=user, profile=user.profile)
        self.send_confirmation_email(user)
        return user

    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its account."""
        exp_date = timezone.now() + timedelta(days=2)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        # Generacion del token
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    def send_confirmation_email(self, user):
        """Send account verification link to given user."""
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! Verify your account'.format(user.username)
        from_email = 'Facebook <Facebook.com>'
        content = render_to_string(
            'account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, 'text/html')
        msg.send()


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
        handle the login request data."""
    
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet.')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()