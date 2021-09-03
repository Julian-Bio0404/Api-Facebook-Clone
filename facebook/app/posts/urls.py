"""Posts URLs."""

# Django
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (CommentViewSet, PostViewSet,
                    create_category, retrieve_category, 
                    create_saved, retrieve_saved, list_saved)


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

router.register(r'posts/(?P<id>[0-9]+)/comments',
                CommentViewSet, basename='comments')

urlpatterns = [
    path('posts/collections/', create_category),
    path('posts/collections/<int:pk>/', retrieve_category),
    path('saved/', list_saved),
    path('saved/<int:pk>/', retrieve_saved),
    path('posts/<int:pk>/saved/', create_saved),
    path('', include(router.urls))
]


