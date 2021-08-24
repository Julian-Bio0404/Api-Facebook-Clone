"""Groups views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from groups.serializers import GroupModelSerializer

# Models
from groups.models import Group, Membership


class GroupeViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """ Group view set."""

    serializer_class = GroupModelSerializer
    lookup_field = "slug_name"

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Group.objects.all()
        if self.action == "list":
            return queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        """Assign group admin."""
        group = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            group=group,
            is_admin=True,
        )