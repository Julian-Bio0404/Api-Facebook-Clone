"""Profiles views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from users.models import Profile
from posts.models import Post

# Serializers
from posts.serializers import PostModelSerializer
from users.serializers import (ProfileDetailModelSerializer,
                               ProfileModelSerializer,
                               UserModelSummarySerializer)


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """ Profile view set.
        Handle list profile, update profile, 
        update profile details and list friends.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
    lookup_field = 'user__username'

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        posts = Post.objects.filter(profile=profile)
        profile_serializer = ProfileModelSerializer(profile).data
        posts_serializer = PostModelSerializer(posts, many=True).data
        data = {
            'profile': profile_serializer,
            'posts': posts_serializer
        }
        return Response(data, status=status.HTTP_200_OK)

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

    @action(detail=True, methods=['get'])
    def friends(self, request, *args, **kwargs):
        """List all friends."""
        profile = self.get_object()
        friends = profile.friends
        serializer = UserModelSummarySerializer(friends, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
