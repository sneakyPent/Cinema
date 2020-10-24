import os

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import *
from django.db.models import Q, QuerySet, Prefetch

from backend.permissions import CustomDjangoModelPermissions
from backend.serializers import *

from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

# from backend.models import Request
from django.contrib.auth.models import User


class MovieViewSet(viewsets.ModelViewSet):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializer
	permission_classes = (CustomDjangoModelPermissions,)


class FavoriteViewSet(viewsets.ModelViewSet):
	queryset = Favorite.objects.all()
	serializer_class = FavoriteSerializer
	permission_classes = (CustomDjangoModelPermissions,)


class CinemaViewSet(viewsets.ModelViewSet):
	queryset = Cinema.objects.all()
	serializer_class = CinemaSerializer
	permission_classes = (CustomDjangoModelPermissions,)
