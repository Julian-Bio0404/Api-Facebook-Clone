"""Posts serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from posts.models import Picture, Post, Shared, Video
from users.models import User

# Serializers
from .media import ImageModelSerializer, VideoModelSerializer


class SharedPostModelSerializer(serializers.ModelSerializer):
    """Shared post model serializer

    Serialize a repost.
    """

    user = serializers.StringRelatedField(read_only=True)
    pictures = ImageModelSerializer(read_only=True, many=True)
    videos = VideoModelSerializer(read_only=True, many=True)  
    tag_friends = serializers.StringRelatedField(required=False, many=True)  

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'user','about', 'pictures',
            'videos', 'privacy', 'feeling',
            'location', 'tag_friends',
            'reactions'
        ]

        read_only_fields = [
            'user', 'reactions'
        ]


class PostModelSerializer(SharedPostModelSerializer):
    """Post model serializer."""

    re_post = SharedPostModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'user','about', 'pictures',
            'videos', 'privacy', 'feeling',
            'location', 'tag_friends',
            'reactions', 'destination',
            'name_destination', 're_post',
            'comments', 'shares'
        ]

        read_only_fields = [
            'user', 'reactions', 
            're_post', 'pictures',
            'videos', 'comments', 
            'shares'
        ]

    def validate(self, data):
        """verify privacy and that only the about, destination and 
        name destination fields are present if it is a repost.
        If it is a post, verify that about, picture or video are present.
        """
        # Verifica privacidad del post
        if ('friends_exc' in self.context['request'].data.keys() 
            and data['privacy'] != 'FRIENDS_EXC'):
            raise serializers.ValidationError(
                'You must specify privacy in FRIENDS_EXC.')

        if ('specific_friends' in self.context['request'].data.keys() 
            and data['privacy'] != 'SPECIFIC_FRIENDS'):
            raise serializers.ValidationError(
                'You must specify privacy in SPECIFIC_FRIENDS.')

        if (data['privacy'] == 'FRIENDS_EXC' 
            and 'friends_exc' not in self.context['request'].data.keys()):
            raise serializers.ValidationError(
                'You must specify a list of usernames in friends_exc.')
        
        if (data['privacy'] == 'SPECIFIC_FRIENDS' 
            and 'specific_friends' not in self.context['request'].data.keys()):
                raise serializers.ValidationError(
                    'You must specify a list of usernames in specific_friends.')

        # Si es un repost, NO permite que se publique con los campos incluidos en fields
        if 'post' in self.context.keys():
            fields = ['pictures', 'videos', 'feeling', 'location', 'tag_friends']
            for i in self.context['request'].data.keys():
                if i in fields:
                    raise serializers.ValidationError(
                        'You can only send an about, privacy, destination or name destination.')
            return data
        else:
            # De lo contrario, verifica que venga al menos un campo de media
            media = ['about', 'pictures', 'videos']
            match = False
            for i in media:
                if i in self.context['request'].data.keys():
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

        # Add friends_except or specific_friends in the privacity configuration
        if data['privacy'] == 'FRIENDS_EXC':
            friends_except = []
            for username in self.context['request'].data['friends_exc']:
                try:
                    friend = User.objects.get(username=username)
                    friends_except.append(friend)
                except User.DoesNotExist:
                    raise serializers.ValidationError(
                        f'The user with username {username} does not exist.')

        elif data['privacy'] == 'SPECIFIC_FRIENDS':
            specific_friends = []
            for username in self.context['request'].data['specific_friends']:
                try:
                    friend = User.objects.get(username=username)
                    specific_friends.append(friend)
                except User.DoesNotExist:
                    raise serializers.ValidationError(
                        f'The user with username {username} does not exist.')

        # Si viene un post en el contexto,
        # se crea un post con el repost
        if 'post' in self.context.keys():
            re_post = self.context['post']

            # Post
            post = Post.objects.create(
                **data, user=user, profile=profile, re_post=re_post)

            # Shared
            Shared.objects.create(
                user=user, post=re_post, about=data['about'])

            # Repost
            re_post.shares += 1
            re_post.save()
        else:
            post = Post.objects.create(**data, user=user, profile=profile)
            try:
                videos = self.context['request'].data.getlist('videos')
                pictures = self.context['request'].data.getlist('pictures')
                
                for image in pictures:
                    picture = Picture.objects.create(content=image)
                    post.pictures.add(picture)
                
                for i in videos:
                    video = Video.objects.create(content=i)
                    post.videos.add(video)
            except AttributeError:
                post.save()

        # Privacy
        if friends_except:
            for friend in friends_except:
                post.friends_exc.add(friend)
        elif specific_friends:
            for friend in specific_friends:
                post.specific_friends.add(friend)
        post.save()
        return post


class CreatePagePostModelSerializer(PostModelSerializer):
    """Create Page Post model serializer."""

    user = serializers.StringRelatedField(read_only=True)

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

    user = serializers.StringRelatedField(read_only=True)

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
