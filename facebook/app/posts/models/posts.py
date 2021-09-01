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
        help_text='write something', max_length=350, blank=True)

    picture = models.ImageField(
        help_text='post picture', upload_to='posts/pictures/', 
        blank=True, null=True)

    video = models.FileField(
        help_text='post video', upload_to='posts/videos/',
        blank=True, null=True)

    # post privacy choices
    POST_PRIVACY = [
        ('PUBLIC', 'Public'),
        ('FRIENDS', 'Friends'),
        ('FRIENDS_EXC', 'Friends_except'),
        ('SPECIFIC_FRIENDS', 'Specific_friends')
    ]

    privacy = models.CharField(
        help_text='privacy of post', 
        max_length=16, choices=POST_PRIVACY, default='FRIENDS')

    # post feeling choices
    FEELING = [
        ('HAPPY', 'happy'), ('LOVED', 'loved'),
        ('EXCITED', 'excited'), ('CRAZY', 'crazy'),
        ('THANKFUL', 'thankful'), ('FANTASTIC', 'fantastic'),
        ('MOTIVED', 'motived'), ('TIRED', 'tired'),
        ('ALONE', 'alone'), ('ANGRY', 'angry'),
        ('SORRY', 'sorry'), ('CONFUSED', 'confused'),
        ('STRONG', 'strong'), ('STRESSED', 'stressed'),
        ('SCARED', 'scared'), ('SICK', 'sick'),
        ('SARCASTIC', 'sarcastic'), ('ANXIOUS', 'anxious')
    ]

    feeling = models.CharField(
        help_text='how you feel', max_length=9, 
        choices=FEELING, blank=True)

    location = models.CharField(
        help_text='where are you?', max_length=60, blank=True)

    tag_friends = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL,
        related_name='tag_friends',
        blank=True, null=True)

    reactions = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)

    # post destination choices
    TYPE_DESTINATION = [
        ('FRIEND', 'friend'), ('GROUP', 'group'),
        ('BIOGRAPHY', 'biography'), ('PAGE', 'page')
    ]

    destination = models.CharField(
        help_text='specify if the post will be published in a group, page, biography of a friend or in your biography',
        max_length=9, choices=TYPE_DESTINATION,
        default='BIOGRAPHY')

    name_destination = models.CharField(
        help_text="name of post's destination",
        max_length=60, blank=True)

    re_post = models.ForeignKey(
        'self', help_text='post to be republished',
        on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """Return about and username"""
        return "{} by @{}".format(self.about, self.user.username)

    class Meta:
        """Meta options."""
        ordering = ['-created']
