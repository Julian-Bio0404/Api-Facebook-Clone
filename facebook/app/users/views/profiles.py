"""Profiles views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from users.models import Profile, ProfileDetail

# Serializers
from users.serializers import (ProfileDetailModelSerializer,
                               ProfileModelSerializer)


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Profile view set.

        Handle list profile, update profile 
        and update profile details."""

    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
    lookup_field = 'user__username'

    @action(detail=True, methods=['put', 'patch'])
    def update_details(self, request, *args, **kwargs):
        """Update profile details."""
        profile = self.get_object()
        details = profile.profiledetail
        partial = request.method == 'PATCH'
        serializer = ProfileDetailModelSerializer(
            details,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
