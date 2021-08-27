"""Groups URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views.groups import GroupeViewSet
from .views.memberships import MembershipViewSet


router = DefaultRouter()
router.register(r'groups', GroupeViewSet, basename="groups")
router.register(
    r'groups/(?P<slug_name>[a-zA-Z0-9_-]+)/members', MembershipViewSet, basename='membership')

urlpatterns = [
    path('', include(router.urls))
]