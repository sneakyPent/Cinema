import os

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import *
from django.db.models import Q, QuerySet, Prefetch

from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from cinema.permissions import CustomDjangoModelPermissions, NotAuthenticatedCreateOnly
from backend.serializers import *

from django.contrib.auth.models import User


class MovieViewSet(viewsets.ModelViewSet):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializer
	permission_classes = (IsAuthenticated ,)

	def get_queryset(self):
		assert self.queryset is not None, (
				"'%s' should either include a `queryset` attribute, "
				"or override the `get_queryset()` method."
				% self.__class__.__name__
		)
		queryset = self.queryset
		user = self.request.user
		if not self.request.user.is_superuser:
			queryset = Movie.objects.filter(cinema__owner=user)
		if isinstance(queryset, QuerySet):
			# Ensure queryset is re-evaluated on each request.
			queryset = queryset.all()
		return queryset

	def list(self, request, *args, **kwargs):
		my_param = request.query_params
		if 'fields' in my_param:
			excl = ['cinema']
			dt = []
			for vr in list(MovieSerializer.Meta.fields):
				if vr not in excl:
					dt.append(vr)
			return Response({'fields': dt})

		if self.request.user.is_superuser:
			self.serializer_class = MovieSerializer
		else:
			self.serializer_class = MovieSerializer
		return super().list(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):
		c = Cinema.objects.get(owner_id=self.request.user.id)
		if c:
			movieInfo = request.data
			m = Movie()
			m.title = movieInfo['title']
			m.startDate = movieInfo['startDate']
			m.endDate = movieInfo['endDate']
			m.category = movieInfo['category']
			c = Cinema.objects.get(owner_id=self.request.user.id)
			m.cinema = c
			m.save()
			return Response(HTTP_200_OK)
		return Response(HTTP_400_BAD_REQUEST)

	def update(self, request, *args, **kwargs):
		m = Movie.objects.get(id=kwargs['pk'])
		c = Cinema.objects.get(owner_id=self.request.user.id)
		if c:
			movieInfo = request.data
			m.title = movieInfo['title']
			m.startDate = movieInfo['startDate']
			m.endDate = movieInfo['endDate']
			m.category = movieInfo['category']
			c = Cinema.objects.get(owner_id=self.request.user.id)
			m.cinema = c
			m.save()
			return Response(HTTP_200_OK)
		return Response(HTTP_400_BAD_REQUEST)


class FavoriteViewSet(viewsets.ModelViewSet):
	queryset = Favorite.objects.all()
	serializer_class = FavoriteSerializer
	permission_classes = (CustomDjangoModelPermissions,)


class CinemaViewSet(viewsets.ModelViewSet):
	queryset = Cinema.objects.all()
	serializer_class = CinemaSerializer
	permission_classes = (CustomDjangoModelPermissions,)


class UserProfileViewSet(viewsets.ModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = (IsAuthenticated | NotAuthenticatedCreateOnly, )

	def list(self, request, *args, **kwargs):
		my_param = request.query_params
		if 'fields' in my_param:
			excl = ['is_staff']
			dt = []
			for vr in list(UserProfileSerializer.Meta.fields):
				if vr not in excl:
					dt.append(vr)
			return Response({'fields': dt})

		if 'nonadmin' in my_param:
			queryset = self.filter_queryset(self.get_queryset())
			queryset = UserProfile.objects.filter(Q(role='owner') | Q(role='user'))
			page = self.paginate_queryset(queryset)
			if page is not None:
				serializer = self.get_serializer(page, many=True)
				return self.get_paginated_response(serializer.data)

			serializer = self.get_serializer(queryset, many=True)
			return Response(serializer.data)
		if self.request.user.is_superuser:
			self.serializer_class = UserProfileSerializer
		else:
			self.serializer_class = UserProfileSerializer
		return super().list(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		u = User.objects.get(id=kwargs['pk'])
		if self.request.user.is_staff:
			userInfo = request.data

			p = UserProfile.objects.get(user=u)
			p.role = userInfo['role']
			u.is_active = userInfo['is_active']
			p.save()
			groups = []
			if p.role == 'user':
				groups = [Group.objects.get(name='User')]
			elif p.role == 'owner':
				groups = [Group.objects.get(name='CinemaOwner')]
			u.groups.set(groups)
			u.save()

			return Response(HTTP_200_OK)
		return Response(HTTP_400_BAD_REQUEST)

	def create(self, request, *args, **kwargs):
		import json
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
			p = UserProfile.objects.get(user=u)
			p.role = formData['role']
			p.save()
			groups = []
			if p.role == 'user':
				groups = [Group.objects.get(name='User')]
			elif p.role == 'owner':
				groups = [Group.objects.get(name='CinemaOwner')]
			u.groups.set(groups)
			u.save()

			p = UserProfile.objects.get(user=u)
			p.role = formData['role']
			p.save()

			return Response(HTTP_200_OK)
		return Response(HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (AllowAny | NotAuthenticatedCreateOnly,)
