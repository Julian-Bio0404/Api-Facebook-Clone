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
    """Profile view set.

    Handle list profile, update profile, 
    update profile details, list friends,
    follow or unfollow users and list
    followers or following.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
    lookup_field = 'user__username'

    def retrieve(self, request, *args, **kwargs):
        """"Return profile and posts of user."""
        profile = self.get_object()
        posts = Post.objects.filter(profile=profile)
        profile_serializer = ProfileModelSerializer(profile).data
        posts_serializer = PostModelSerializer(posts, many=True).data
        data = {'profile': profile_serializer, 'posts': posts_serializer}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def update_details(self, request, *args, **kwargs):
        """Update profile details."""
        profile = self.get_object()
        details = profile.profiledetail
        partial = request.method == 'PATCH'
        serializer = ProfileDetailModelSerializer(
            details, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def friends(self, request, *args, **kwargs):
        """List all friends."""
        profile = self.get_object()
        friends = profile.friends
        serializer = UserModelSummarySerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwargs):
        """Follow or unfollow a user."""
        profile = self.get_object()
        followers = profile.followers.all()
        user = request.user

        if user == profile.user:
            data = {'message': "You can't follow yourself"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        if user not in followers:
            profile.followers.add(user)
            user.profile.following.add(profile.user)
            data = {
                'message': f'You started following to {profile.user.username}'}
        else:
            profile.followers.remove(user)
            user.profile.following.remove(user)
            data = {
                'message': f'you stopped following to {profile.user.username}'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers(self, request, *args, **kwargs):
        """List all followers."""
        profile = self.get_object()
        followers = profile.followers
        serializer = UserModelSummarySerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def following(self, request, *args, **kwargs):
        """List all following."""
        profile = self.get_object()
        following = profile.following
        serializer = UserModelSummarySerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
