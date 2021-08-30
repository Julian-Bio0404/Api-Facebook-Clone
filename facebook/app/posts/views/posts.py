"""Posts views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from posts.models import Post, ReactionPost

# Serializers
from posts.serializers import (PostModelSerializer,
                               ReactionPostModelSerializer,
                               ReactionPostModelSummarySerializer)


class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """ Post view set.
        Handle list, create, update, destroy
        and sharing post.
    """

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    def create(self, request):
        """Create a post."""
        serializer = PostModelSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def react(self, request, *args, **kwargs):
        """Create a post's reaction."""
        post = self.get_object()
        serializer = ReactionPostModelSerializer(
            data=request.data,
            context={
                'user': request.user,
                'post': post}
        )
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        except AssertionError:
            return Response(
                {'message': 'The reaction has been delete.'}, 
                status=status.HTTP_200_OK
            )

    @action(detail=True, methods=['get'])
    def reactions(self, request, *args, **kwargs):
        """List all post's reactions."""
        post = self.get_object()
        reactions = ReactionPost.objects.filter(post=post)
        serializer = ReactionPostModelSummarySerializer(reactions, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def shared(self, request, *args, **kwargs):
        """Handles share post."""
        post = self.get_object()
        serializer = PostModelSerializer(
            data=request.data,
            context={
                'user': request.user,
                'post': post}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
