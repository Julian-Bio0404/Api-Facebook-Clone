"""Groups views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import IsAuthenticated
from app.groups.permissions import IsGroupAdmin, IsPublicGroup

# Models
from app.groups.models import Group, Membership
from app.posts.models import Post

# Serializers
from app.groups.serializers import GroupModelSerializer
from app.posts.serializers import PostModelSerializer


class GroupeViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    Group view set.
    Handle list, detail, update, partial update, 
    delete groups and list group's posts.
    """

    serializer_class = GroupModelSerializer
    lookup_field = 'slug_name'
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('name', 'created')
    ordering = ('-members__count',)
    filter_fields = ('is_public',)  # DjangoFilterBackend

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['retrieve']:
            permissions.append(IsPublicGroup)
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsGroupAdmin)
        return [permission() for permission in permissions]

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Group.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        """Assign group admin."""
        group = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user, profile=profile, group=group, 
            is_admin=True, is_active=True)
    
    @action(detail=True, methods=['get'])
    def posts(self, request, *args, **kwargs):
        """List all grop's posts."""
        group = self.get_object()

        if group.is_public == False:
            try:
                Membership.objects.get(
                    user=request.user, group=group, is_active=True)
            except Membership.DoesNotExist:
                data = {'message': 'You do not have permission to perform this action.'}
                return Response(data, status=status.HTTP_403_FORBIDDEN)

        posts = Post.objects.filter(
            destination='GROUP', name_destination=group.slug_name)
        data = PostModelSerializer(posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)
