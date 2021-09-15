"""Profiles views."""

# Django
from django.db.models import Q

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from app.users.permissions import IsProfileOwner

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
    update profile details, follow or unfollow 
    users and list followers, following and friends.
    """

    queryset = Profile.objects.filter(user__is_verified=True)
    serializer_class = ProfileModelSerializer
    lookup_field = 'user__username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['retrieve']:
            permissions = [AllowAny]
        elif self.action in ['update', 'partial_update']:
           permissions = [IsAuthenticated, IsProfileOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

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
    def posts(self, request, *args, **kwargs):
        """List profile's posts. 
        Restric according to the user requesting and privacy of posts.
        """
        profile = self.get_object()
        friends = list(profile.friends.all())

        if request.user.profile == profile:
            posts = Post.objects.filter(
                Q(profile=profile, destination='BIOGRAPHY') |
                Q(destination='FRIEND', name_destination=profile.user.username))
        elif request.user in friends:
            posts = Post.objects.filter(
                Q(profile=profile, destination='BIOGRAPHY', privacy='PUBLIC')
                | Q(profile=profile, destination='BIOGRAPHY', privacy='FRIENDS')
                | Q(profile=profile, destination='BIOGRAPHY', specific_friends__in=[request.user])
                | Q(destination='FRIEND', name_destination=profile.user.username, privacy='FRIENDS')
                | Q(destination='FRIEND', name_destination=profile.user.username, specific_friends__in=[request.user])
                | Q(profile=profile, destination='BIOGRAPHY', privacy='FRIENDS_EXC')
                | Q(destination='FRIEND', name_destination=profile.user.username, privacy='FRIENDS_EXC')
            ).exclude(
                Q(friends_exc__in=[request.user]))
        else:
            posts = Post.objects.filter(
                Q(profile=profile, destination='BIOGRAPHY', privacy='PUBLIC') |
                Q(destination='FRIEND', name_destination=profile.user.username, privacy='PUBLIC'))

        data = PostModelSerializer(posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)

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
        profile.save()
        user.save()
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
