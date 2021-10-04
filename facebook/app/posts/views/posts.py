"""Posts views."""

# Django
from django.db.models import Q

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from app.posts.permissions import IsFriend, IsPostOwner

# Models
from app.posts.models import CategorySaved, Post, ReactionPost, Saved, Shared

# Serializers
from app.posts.serializers import (PostModelSerializer,
                                   ReactionPostModelSerializer,
                                   ReactionPostModelSummarySerializer,
                                   SavedPostModelSerializer,
                                   SharedModelSerializer)


class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Post view set.
    Handle list, create, update, destroy,
    sharing, list shares, react to a post
    list post's reactions and post saving.
    """

    serializer_class = PostModelSerializer

    def get_queryset(self):
        """Restrict list to public or friend's posts."""
        queryset = Post.objects.all()
        user = self.request.user
        friends = user.profile.friends.all()
        if self.action == 'list':
            queryset = Post.objects.filter(
                Q(user=user) | Q(privacy='PUBLIC') | Q(user__in=friends, privacy='FRIENDS') 
                | Q(user__in=friends, privacy='SPECIFIC_FRIENDS', specific_friends__in=[user])
                | Q(specific_friends__in=[user])).exclude(Q(friends_exc__in=[user]))
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            'retrieve', 'react', 'reactions', 'share', 'post_shares', 'saved']:
            permissions = [IsFriend]
        elif self.action in ['update', 'partial_update', 'destroy']:
           permissions = [IsAuthenticated, IsPostOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

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
            data=request.data, context={'user': request.user, 'post': post, 'request': request})
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
    
    @action(detail=True, methods=['post'])
    def saved(self, request, *args, **kwargs):
        """Handles post saving."""
        post = self.get_object()
        
        # Valida que el post y categoria existan
        try:
            saved_category = CategorySaved.objects.get(
                user=request.user, name=request.data['name'])
        except CategorySaved.DoesNotExist:
            data = {'message': 'The category does not exist.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        # Valida que aun no exista el post guardado
        try:
            Saved.objects.get(user=request.user, post=post)
            data = {'message': 'The saved already exists.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Saved.DoesNotExist:
            serializer = SavedPostModelSerializer(
                data=request.data, 
                context={
                    'user': request.user, 'post': post, 'saved_category': saved_category})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
