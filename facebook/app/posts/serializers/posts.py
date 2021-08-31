"""Posts serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from posts.models import Post, Shared

# Serializers
from users.serializers import UserModelSummarySerializer


class SharedPostModelSerializer(serializers.ModelSerializer):
    """Shared post model serializer."""

    user = UserModelSummarySerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'user','about', 'picture',
            'video', 'privacy', 'feeling',
            'location', 'tag_friends',
            'reactions'
        ]

        read_only_fields = [
            'user', 'reactions'
        ]


class PostModelSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    user = UserModelSummarySerializer(read_only=True)
    re_post = SharedPostModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'user','about', 'picture',
            'video', 'privacy', 'feeling',
            'location', 'tag_friends',
            'reactions', 'destination',
            'name_destination', 're_post'
        ]

        read_only_fields = [
            'user', 'reactions', 
            're_post'
        ]

    def validate(self, data):
        """Verify that about, picture or video are present."""
        if self.context['post']:
            return data
        else:
            media = ['picture', 'video', 'about']
            match = False
            for i in media:
                if i in data:
                    match = True
                    break
            if match == False:
                raise serializers.ValidationError(
                    'You must include an about, picture or video.')
            return data

    def create(self, data):
        """Create a post."""
        user = self.context['user']
        profile = user.profile
        if self.context['post']:
            post = Post.objects.create(
                **data, user=user, 
                profile=profile, 
                re_post=self.context['post'])
        else:
            post = Post.objects.create(**data, user=user, profile=profile)
            post.save()
        return post


class CreatePagePostModelSerializer(PostModelSerializer):
    """Create Page Post model serializer."""

    user = serializers.StringRelatedField()

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'user','about', 'picture',
            'video', 'privacy', 'feeling',
            'location','reactions', 'destination',
            'name_destination'
        ]

        read_only_fields = [
            'user', 'reactions', 
            'privacy', 'destination'
            'name_destination'
        ]

    def create(self, data):
        """Create a post."""
        user = self.context['user']
        profile = user.profile
        post = Post.objects.create(
            **data, user=user, 
            profile=profile, 
            privacy=self.context['privacy'],
            destination=self.context['destination'], 
            name_destination=self.context['name_destination'])
        post.save()
        return post


class SharedModelSerializer(serializers.ModelSerializer):
    """Shared model serializer."""

    user = serializers.StringRelatedField()

    class Meta:
        """Meta options."""
        model = Shared
        fields = [
            'user', 'about', 
            'post'
        ]

        read_only_fields = [
            'user', 'post'
        ]
