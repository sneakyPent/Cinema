from rest_framework import routers

from backend.viewsets import CinemaViewSet
from backend.viewsets import MovieViewSet
from backend.viewsets import FavoriteViewSet
from backend.viewsets import UserViewSet
from backend.viewsets import UserProfileViewSet

router = routers.DefaultRouter()

router.register(r'Cinema', CinemaViewSet)
router.register(r'Movie', MovieViewSet)
router.register(r'Favorite', FavoriteViewSet)
router.register(r'User', UserViewSet)
router.register(r'UserProfile', UserProfileViewSet)
