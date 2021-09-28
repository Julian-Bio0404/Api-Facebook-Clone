"""Notifications tasks."""

# Celery
from celery import shared_task

# Models
from app.fbpages.models import Page
from app.groups.models import Group
from app.notifications.models import Notification
from app.posts.models import Post, Comment
from app.users.models import User


@shared_task 
def create_notification(user1_pk, user2_pk, type, obj_pk):
    """
    Create notifications.
    user1_pk: pk of the issuing user the notification,
    user2_pk: pk of the receiving user the notification
    """
    issuing_user = User.objects.get(pk=user1_pk)
    receiving_user = User.objects.get(pk=user2_pk)  
    message = f'{issuing_user.username} '

    if type == 'Group Invitation':
        group = Group.objects.get(pk=obj_pk)
        message += f'sent you an invitation to join the {group.slug_name} group.'
    elif type == 'Page Invitation':
        page = Page.objects.get(pk=obj_pk)
        message += f'sent you an invitation to like the {page.slug_name} page.'
    elif type == 'Reaction Post':
        post = Post.objects.get(pk=obj_pk)
        message += f'reacted to your post {post.about}.'
    elif type == 'Post':
        post = Post.objects.get(pk=obj_pk)
        message += f'posted on your biography {post.about}.'
    elif type == 'Comment Post':
        message += 'commented on your post.'
    elif type == 'Reaction Comment':
        comment = Comment.objects.get(pk=obj_pk)
        message += f'reacted to your comment "{comment.text}".'
    elif type == 'Friend Request':
        message += f'sent you a friend request.'
    elif type == 'Friend Accept':
        message += f'accepted your friend request.'
        
    notification = Notification.objects.create(
        issuing_user=issuing_user, 
        receiving_user=receiving_user, 
        object_id=obj_pk, message=message)

    return notification
