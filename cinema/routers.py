from rest_framework import routers

from backend.viewsets import CinemaViewSet
from backend.viewsets import MovieViewSet
from backend.viewsets import FavoriteViewSet
from backend.viewsets import RequestViewSet

router = routers.DefaultRouter()

router.register(r'Request', RequestViewSet)
router.register(r'Cinema', CinemaViewSet)
router.register(r'Movie', MovieViewSet)
router.register(r'Favorite', FavoriteViewSet)
