"""Users URLs."""

#Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

#Views
from .views import UserViewSet, ProfileViewSet, FriendRequestViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profile', ProfileViewSet, basename='profiles')
router.register(r'profile/(?P<username>[a-zA-Z0-9]+)/friend_requests', 
                FriendRequestViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls))
]