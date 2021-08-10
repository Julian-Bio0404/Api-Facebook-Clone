"""Profiles views."""

# Django REST framework
from rest_framework import mixins, viewsets

# Models
from users.models import Profile

# Serializers
from users.serializers import ProfileModelSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Profile view set.
    Handle signup, login and account verification."""

    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
    lookup_field = 'user__username'