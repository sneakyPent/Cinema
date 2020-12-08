from rest_framework import routers

from backend.viewsets import CinemaViewSet
from backend.viewsets import MovieViewSet
from backend.viewsets import FavoriteViewSet
from backend.viewsets import RequestViewSet
from backend.viewsets import NotificationsViewSet
from backend.viewsets import UserSubscriptionsViewSet

router = routers.DefaultRouter()

router.register(r'Request', RequestViewSet)
router.register(r'Cinema', CinemaViewSet)
router.register(r'Movie', MovieViewSet)
router.register(r'Favorite', FavoriteViewSet)
router.register(r'Subscriptions', UserSubscriptionsViewSet)
router.register(r'Notifications', NotificationsViewSet)
