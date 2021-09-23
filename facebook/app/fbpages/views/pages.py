"""Fbpages views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from app.fbpages.permissions import IsCreatorOrAdminPage, IsCreatorPage

# Serializers
from app.fbpages.serializers import (CreatePageInvitation, PageModelSerializer,
                                     PageDetailModelSerializers, PageInvitationSerializer)

from app.posts.serializers import (CreatePagePostModelSerializer,
                                   PostModelSerializer)

from app.users.serializers import UserModelSummarySerializer

# Models
from app.fbpages.models import Page
from app.posts.models import Post
from app.users.models import User


class PageViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Page view set."""

    queryset = Page.objects.all()
    serializer_class = PageModelSerializer
    lookup_field = 'slug_name'
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('slug_name', 'name', 'category__name')
    ordering_fields = ('name', 'created')

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['retrieve', 'posts']:
            permissions = [AllowAny]
        elif self.action in [
            'update', 'partial_update', 'update_details', 'create_post']:
           permissions = [IsAuthenticated, IsCreatorOrAdminPage]
        elif self.action in ['add_admin', 'remove_admin']:
            permissions = [IsCreatorPage]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    def perform_destroy(self, instance):
        """Delete page and page's posts."""
        posts = Post.objects.filter(
            destination='PAGE', name_destination=instance.slug_name)
        posts.delete()
        instance.delete()

    def create(self, request):
        """Handles page creation."""
        serializer = PageModelSerializer(
            data=request.data,
            context={'creator': request.user, 'category': request.data['category']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def create_post(self, request, *args, **kwargs):
        """Handles page's post creation."""
        page = self.get_object()
        serializer = CreatePagePostModelSerializer(
            data=request.data,
            context={
                'user': request.user, 'destination': 'PAGE',
                'name_destination': page.slug_name, 'privacy': 'PUBLIC'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def update_details(self, request, *args, **kwargs):
        """Update page details."""
        page = self.get_object()
        details = page.pagedetail
        partial = request.method == 'PATCH'
        serializer = PageDetailModelSerializers(
            details, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def posts(self, request, *args, **kwargs):
        """List all page's posts."""
        page = self.get_object()
        posts = Post.objects.filter(
            destination='PAGE', name_destination=page.slug_name)
        data = PostModelSerializer(posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers(self, request, *args, **kwargs):
        """List all page's followers."""
        page = self.get_object()
        followers = page.page_followers
        serializer = UserModelSummarySerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwargs):
        """Follow or unfollow a page."""
        page = self.get_object()
        followers = page.page_followers.all()
        user = request.user

        if user not in followers:
            page.page_followers.add(user)
            data = {
                'message': f'You started following to {page.name}'}
        else:
            page.page_followers.remove(user)
            data = {
                'message': f'you stopped following to {page.name}'}
        page.save()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_admin(self, request, *args, **kwargs):
        """Add admin to a page."""
        page = self.get_object()

        if 'username' in request.data.keys():
            try:
                new_admin = User.objects.get(username=request.data['username'])
            except User.DoesNotExist:
                data = {'message': 'User does not exist.'}
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            page.admins.add(new_admin)
            page.save()
            admins = UserModelSummarySerializer(page.admins, many=True).data
            data = {
                'message': f'{new_admin.username} is a new admin of {page.name}.',
                'admins': admins}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'You must send a username.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_admin(self, request, *args, **kwargs):
        """Remove admin from a page."""
        page = self.get_object()

        if 'username' in request.data.keys():
            try:
                admin = User.objects.get(username=request.data['username'])
            except User.DoesNotExist:
                data = {'message': 'User does not exist.'}
                return Response(data, status=status.HTTP_404_NOT_FOUND)

            if admin in page.admins.all():
                page.admins.remove(admin)
                page.save()
                data = {'message': f'{admin.username} admin removed.'}
            else:
                data = {'message': 'User is not a admin.'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'You must send a username.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'])
    def invitation(self, request, *args, **kwargs):
        """Handle the sending of page invitations."""
        page = self.get_object()
        serializer = CreatePageInvitation(
            data=request.data, context={'page': page, 'request': request})
        serializer.is_valid(raise_exception=True)
        page_invitation = serializer.save()
        data = PageInvitationSerializer(page_invitation).data
        return Response(data, status=status.HTTP_201_CREATED)
