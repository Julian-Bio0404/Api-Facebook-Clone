"""Users URLs."""

#Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

#Views
from .views import UserViewSet, ProfileViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profile', ProfileViewSet, basename='profiles')

urlpatterns = [

    path('', include(router.urls)),
    path('', include(router.urls))
    
]