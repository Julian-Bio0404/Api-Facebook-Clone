"""Notification Views."""

# Django REST framework
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from app.fbpages.models import PageInvitation
from app.notifications.models import Notification
from app.posts.models import Post, Comment
from app.users.models import FriendRequest, Profile

# Serializers
from app.fbpages.serializers import PageInvitationSerializer
from app.notifications.serializers import NotificationModelSerializer
from app.posts.serializers import PostModelSerializer, CommentModelSerializer
from app.users.serializers import FriendRequestModelSerializer, ProfileModelSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    """List all notifications of receiving user."""
    notifications = Notification.objects.filter(
        receiving_user=request.user)
    data = NotificationModelSerializer(notifications, many=True).data
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detail_notification(request, pk):
    """Retrieve notification."""
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        data = {'message': 'The notification does not exist.'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    notif_type = notification.notification_type
    object_id = notification.object_id

    try:
        if notif_type in ['Reaction Post', 'Post']:
            obj = Post.objects.get(pk=object_id)
            data = PostModelSerializer(obj).data
        elif notif_type in ['Comment Post', 'Reaction Comment', 'Mention']:
            obj = Comment.objects.get(pk=object_id)
            data = CommentModelSerializer(obj).data
        elif notif_type == 'Friend Request':
            obj = FriendRequest.objects.get(pk=object_id)
            data = FriendRequestModelSerializer(obj).data
        elif notif_type == 'Friend Accept':
            obj = Profile.objects.get(pk=object_id)
            data = ProfileModelSerializer(obj).data
        elif notif_type == 'Page Invitation':
            obj = PageInvitation.objects.get(pk=object_id)
            data = PageInvitationSerializer(obj).data
        else:
            data = NotificationModelSerializer(notification).data
        return Response(data, status=status.HTTP_200_OK)
    except Exception:
        data = {'message': 'Content not available.'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)
