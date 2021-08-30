"""Fbpages views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import UserModelSummarySerializer

# Serializers
from fbpages.serializers import PageModelSerializer
from posts.models import Post
from posts.serializers import (CreatePagePostModelSerializer,
                               PostModelSerializer)

# Models
from fbpages.models import Page


class PageViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Page view set."""

    queryset = Page.objects.all()
    serializer_class = PageModelSerializer
    lookup_field = 'slug_name'

    def perform_destroy(self, instance):
        """Delete page and page's posts."""
        posts = Post.objects.filter(
            destination='PAGE', name_destination=instance.name)
        posts.delete()
        instance.delete()

    def create(self, request):
        """Handles page creation."""
        serializer = PageModelSerializer(
            data=request.data,
            context={
                'creator': request.user,
                'category': request.data['category']}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def create_post(self, request, *args, **kwargs):
        """Handles page's post creation."""
        page = self.get_object()
        serializer = CreatePagePostModelSerializer(
            data=request.data,
            context={
                'user': request.user,
                'destination': 'PAGE',
                'name_destination': page.name,
                'privacy': 'PUBLIC'}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def posts(self, request, *args, **kwargs):
        """List all page's posts."""
        page = self.get_object()
        posts = Post.objects.filter(
            destination='PAGE', name_destination=page.name)
        data = PostModelSerializer(posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers(self, request, *args, **kwargs):
        """List all page's followers."""
        page = self.get_object()
        followers = page.page_followers
        serializer = UserModelSummarySerializer(followers, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwargs):
        """Follow or unfollow a user."""
        page = self.get_object()
        followers = page.page_followers.all()
        user = request.user
        if user not in followers:
            page.page_followers.add(user)
            data = {
                'message': f'You started following to {page.name}'}
        else:
            page.page_followers.remove(user)
            data = {
                'message': f'you stopped following to {page.name}'}
        return Response(data, status=status.HTTP_200_OK)
