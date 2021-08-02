"""Post model."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel


class Post(FbModel):
    """Post model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    about = models.CharField(
        help_text='write something', 
        max_length=350, 
        blank=True
    )

    picture = models.ImageField(
        help_text='post picture', 
        upload_to='posts/pictures/', 
        blank=True, null=True
    )

    # post privacy choices
    POST_PRIVACY = [
        ('PUBLIC', 'Public'),
        ('FRIENDS', 'Friends'),
        ('FRIENDS_EXC', 'Friends_except'),
        ('SPECIFIC_FRIENDS', 'Specific_friends')
    ]

    privacy = models.CharField(
        help_text='privacy of post', 
        max_length=16, 
        choices=POST_PRIVACY, 
        default='FRIENDS'
    )

    # post feeling choices
    FEELING = [
        ('HAPPY', 'happy'), ('LOVED', 'loved'),
        ('EXCITED', 'excited'), ('CRAZY', 'crazy'),
        ('THANKFUL', 'thankful'), ('FANTASTIC', 'fantastic'),
        ('MOTIVED', 'motived'), ('TIRED', 'tired'),
        ('ALONE', 'alone'), ('ANGRY', 'angry'),
        ('SORRY', 'sorry'), ('CONFUSED', 'confused'),
        ('STRONG', 'strong'), ('STRESSED', 'stressed'),
        ('SCARED', 'scared')
    ]

    feeling = models.CharField(
        help_text='how you feel',  
        max_length=9, 
        choices=FEELING,
        blank=True
    )

    location = models.CharField(
        help_text='where are you?',
        max_length=60,
        blank=True
    )

    tag_friends = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='tag_friends',
        blank=True,
        null=True
    )

    reactions = models.IntegerField(default=0)

    #group = models.ForeignKey(
    #    'groups.Group',
    #    on_delete=models.SET_NULL,
    #    blank=True,
    #    null=True
    #)