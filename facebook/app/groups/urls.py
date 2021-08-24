"""Groups URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views.groups import GroupeViewSet


router = DefaultRouter()
router.register(r'groups', GroupeViewSet, basename="groups")

urlpatterns = [
    path("", include(router.urls))
]