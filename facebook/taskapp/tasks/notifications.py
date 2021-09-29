"""Notifications tasks."""

# Celery
from celery import shared_task

# Models
from app.fbpages.models import Page
from app.groups.models import Group
from app.notifications.models import Notification
from app.posts.models import Post, Comment, ReactionPost, ReactionComment
from app.users.models import User


@shared_task 
def create_notification(user1_pk, user2_pk, type, obj_pk, comment_pk=None):
    """
    Create notifications.
    user1_pk: pk of the issuing user the notification,
    user2_pk: pk of the receiving user the notification,
    type: tyoe of the notification,
    obj_pk: pk of the object on which the notification was generated,
    comment_pk: pk of the comment.
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

    if type in ['Reaction Post', 'Comment Post', 'Reaction Comment']:

        # Flujo de edicion del mensaje de notificacion en funcion de quien 
        # genero la notificacion y la cantidad de usaurios que han interactuado 
        try:
            notification = Notification.objects.get(
                receiving_user=receiving_user, 
                notification_type=type, object_id=obj_pk)
            
            # Los querys obtienen el numero de los diferentes usuarios 
            # que han comentado o reaccionado, excluyendo al usuario
            # dueno del objeto(post o comentario)
            if type == 'Reaction Post':
                post_reactions = ReactionPost.objects.filter(
                    post=post).exclude(user=receiving_user).values('user').distinct().count() - 1
                if post_reactions == 1:
                    message = f'{issuing_user.username} and {notification.issuing_user.username} reacted to your post.'
                elif post_reactions > 1:
                    message = f'{issuing_user.username} and {post_reactions} other people reacted to your post.'

            elif type == 'Comment Post':
                comment = Comment.objects.get(pk=comment_pk)
                post = comment.post
                comments = Comment.objects.filter(
                    post=post).exclude(user=receiving_user).values('user').distinct().count() - 1
                if comments == 1:
                    message = f'{issuing_user.username} and {notification.issuing_user.username} commented on your post.'
                elif comments > 1:
                    message = f'{issuing_user.username} and {comments} other people commented on your post.'

            elif type == 'Reaction Comment':
                comment_reactions = ReactionComment.objects.filter(
                    comment=comment).exclude(user=receiving_user).values('user').distinct().count() - 1
                if comment_reactions == 1:
                    message = f'{issuing_user.username} and {notification.issuing_user.username} reacted to your comment.'
                elif comment_reactions > 1:
                    message = f'{issuing_user.username} and {comment_reactions} other people reacted to your comment.'

            if issuing_user.username == notification.issuing_user.username:
                message = notification.message
            
            # Si existe la notificacion, esta se actualiza
            # de lo contrario, se creara
            notification.issuing_user = issuing_user
            notification.message = message
            notification.save()
            return notification
        except Notification.DoesNotExist:
            pass

    notification = Notification.objects.create(
            issuing_user=issuing_user, receiving_user=receiving_user, 
            notification_type=type, object_id=obj_pk, message=message)
    return notification
