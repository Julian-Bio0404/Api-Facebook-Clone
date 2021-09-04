"""Posts views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from posts.models import Post, ReactionPost, Shared

# Serializers
from posts.serializers import (PostModelSerializer,
                               ReactionPostModelSerializer,
                               ReactionPostModelSummarySerializer,
                               SharedModelSerializer)


class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Post view set.

    Handle list, create, update, destroy
    and sharing post.
    """

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    def create(self, request):
        """Handles post creation."""
        serializer = PostModelSerializer(
            data=request.data, context={'user': request.user, 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def react(self, request, *args, **kwargs):
        """Handles post's reaction."""
        post = self.get_object()
        serializer = ReactionPostModelSerializer(
            data=request.data, context={'user': request.user, 'post': post})
            
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AssertionError:
            return Response({'message': 'The reaction has been delete.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def reactions(self, request, *args, **kwargs):
        """List all post's reactions."""
        post = self.get_object()
        reactions = ReactionPost.objects.filter(post=post)
        serializer = ReactionPostModelSummarySerializer(reactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def share(self, request, *args, **kwargs):
        """Handles share post."""
        post = self.get_object()
        serializer = PostModelSerializer(
            data=request.data, context={'user': request.user,'post': post})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def post_shares(self, request, *args, **kwargs):
        """Handles list shares of a post."""
        post = self.get_object()
        shares = Shared.objects.filter(post=post)
        serializer = SharedModelSerializer(shares, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
