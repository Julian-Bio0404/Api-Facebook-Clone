"""Fbpages URLs."""

#Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

#Views
from .views import PageViewSet


router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='pages')

urlpatterns = [
    path('', include(router.urls)),    
]