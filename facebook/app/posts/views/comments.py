"""Comments views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from posts.models import Comment, Post, ReactionComment

# Serializers
from posts.serializers import (CommentModelSerializer, 
                               ReactionCommentModelSerializer,
                               ReactionCommentModelSummarySerializer)

class CommentViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """ Comment view set.
        Handle list, create, update and destroy comment.
    """
    serializer_class = CommentModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the post exists."""
        id = kwargs['id']
        self.object = get_object_or_404(Post, id=id)
        return super(CommentViewSet, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """Return post's comments."""
        comments = Comment.objects.filter(post=self.object)
        return comments
    
    @action(detail=False, methods=['post'])
    def comment(self, request, *args, **kwargs):
        """Create a comment."""
        serializer = CommentModelSerializer(
            data=request.data,
            context={
                'user': request.user,
                'post': self.object
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def react(self, request, *args, **kwargs):
        """Create a comment's reaction."""
        comment = self.get_object()
        serializer = ReactionCommentModelSerializer(
            data=request.data,
            context={
                'user': request.user,
                'comment': comment
            }
        )
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        except AssertionError:
            return Response(
                {'message': "The comment's reaction has been delete."}, 
                status=status.HTTP_200_OK
            )
    
    @action(detail=True, methods=['get'])
    def reactions(self, request, *args, **kwargs):
        """List all comment's reactions."""
        comment = self.get_object()
        reactions = ReactionComment.objects.filter(comment=comment)
        serializer = ReactionCommentModelSummarySerializer(reactions, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
