"""Friend requests views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from app.users.permissions import IsRequestedUser

# Models
from users.models import FriendRequest, User

# Serializers
from users.serializers import (AcceptFriendRequestSerializer,
                               FriendRequestModelSerializer,
                               ProfileModelSerializer)


class FriendRequestViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """Friend request view set.

    Handle the sending, acceptance and list of friend requests.
    """

    serializer_class = ProfileModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['retrieve', 'confirm', 'destroy']:
           permissions = [IsAuthenticated, IsRequestedUser]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exists."""
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(FriendRequestViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return the friend's request of user."""
        friend_request = FriendRequest.objects.filter(requested_user=self.user)
        return friend_request

    def create(self, request, *args, **kwargs):
        """handles the sending of friend requests."""
        serializer = FriendRequestModelSerializer(
            data=request.data,
            context={'requesting_user': request.user, 'requested_user': self.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """Friend request details."""
        friend_request = self.get_object()
        serializer = FriendRequestModelSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        """List all user's friend request."""
        if request.user == self.user:
            friend_requests = FriendRequest.objects.filter(
                requested_user=request.user)
            serializer = FriendRequestModelSerializer(friend_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'You do not have permission for this action.'}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def confirm(self, request, *args, **kwargs):
        """Handle the confirmation of friend request."""
        friend_request = self.get_object()
        serializer = AcceptFriendRequestSerializer(
            data=request.data, context={'friend_request': friend_request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = FriendRequestModelSerializer(friend_request).data
        return Response(data, status=status.HTTP_200_OK)
