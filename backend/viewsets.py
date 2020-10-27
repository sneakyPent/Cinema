import os

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import *
from django.db.models import Q, QuerySet, Prefetch

from backend.permissions import CustomDjangoModelPermissions, NotAuthenticatedCreateOnly
from backend.serializers import *

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


class UserViewSet(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()
	permission_classes = (CustomDjangoModelPermissions | NotAuthenticatedCreateOnly,)

	def create(self, request, *args, **kwargs):
		import json
		# return Response(status=HTTP_202_ACCEPTED)
		print(json.loads(request.data['formData']))
		if request.data['Type'] == 'Registration':
			formData = json.loads(request.data['formData'])

			u = User()
			u.first_name = formData['name']
			u.last_name = formData['surname']
			u.email = formData['email']
			u.username = formData['username']
			u.set_password(formData['password'])
			u.is_active = False
			u.save()
			groups = []
			if formData['role'] == 'user':
				groups = [Group.objects.get(name='User')]
			elif formData['role'] == 'owner':
				groups = [Group.objects.get(name='CinemaOwner')]
			u.groups.set(groups)
			u.save()

			return Response(HTTP_200_OK)
		return Response(HTTP_400_BAD_REQUEST)
























