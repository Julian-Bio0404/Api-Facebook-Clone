"""Posts views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from posts.models import Post

# Serializers
from posts.serializers import PostModelSerializer


class PostViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Post view set.

        Handle list, create, update and destroy post."""

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['post'])
    def create_post(self, request):
        """Create a post."""
        serializer = PostModelSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
