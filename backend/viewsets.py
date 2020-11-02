import os

from rest_framework import filters, status, generics
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


class MovieViewSet(viewsets.ModelViewSet ):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializer
	permission_classes = (IsAuthenticated, )
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'category', 'cinema__name']

	def get_queryset(self):
		assert self.queryset is not None, (
				"'%s' should either include a `queryset` attribute, "
				"or override the `get_queryset()` method."
				% self.__class__.__name__
		)
		user = self.request.user
		up = UserProfile.objects.get(id=user.id)
		startDate = self.request.query_params.get('startDate', None)
		if startDate is not None:
			print(startDate)
			queryset = self.queryset
		elif self.request.user.is_superuser or up.role == 'user':
			queryset = self.queryset
		elif up.role == 'owner':
			queryset = Movie.objects.filter(cinema__owner=user)
		else:
			queryset = self.queryset
		if isinstance(queryset, QuerySet):
			# Ensure queryset is re-evaluated on each request.
			queryset = queryset.all()
		return queryset

	def list(self, request, *args, **kwargs):
		my_param = request.query_params
		up = UserProfile.objects.get(id=self.request.user.id)
		excl = []
		if self.request.user.is_superuser or up.role == 'user':
			excl = []
		elif up.role == 'owner':
			excl = ['cinema']
		if 'fields' in my_param:
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
			return Response(HTTP_200_OK, status=status.HTTP_200_OK)
		return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)

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
			return Response(HTTP_200_OK, status=status.HTTP_200_OK)
		return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)


class FavoriteViewSet(viewsets.ModelViewSet):
	queryset = Favorite.objects.all()
	serializer_class = FavoriteSerializer
	permission_classes = (IsAuthenticated | NotAuthenticatedCreateOnly, )
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]

	def list(self, request, *args, **kwargs):
		my_param = request.query_params
		up = UserProfile.objects.get(id=self.request.user.id)
		if self.request.user.is_superuser or up.role == 'user':
			if 'titleList' in my_param:
				f_titles = Favorite.objects.filter(user=self.request.user).values_list('movie__title')
				dt = []
				for vr in f_titles:
					dt.append(vr[0])
				return Response({'title': dt})
		else:

			return Response(HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

		if self.request.user.is_superuser:
			self.serializer_class = FavoriteSerializer
		else:
			self.serializer_class = FavoriteSerializer
		return super().list(request, *args, **kwargs)

	def get_queryset(self):
		assert self.queryset is not None, (
				"'%s' should either include a `queryset` attribute, "
				"or override the `get_queryset()` method."
				% self.__class__.__name__
		)
		user = self.request.user
		up = UserProfile.objects.get(id=user.id)

		if self.request.user.is_superuser:
			queryset = self.queryset
		elif up.role == 'user':
			queryset = Favorite.objects.filter(user=user.id)
		else:
			queryset = self.queryset
		if isinstance(queryset, QuerySet):
			# Ensure queryset is re-evaluated on each request.
			queryset = queryset.all()
		return queryset

	def create(self, request, *args, **kwargs):
		rq_m = Movie.objects.get(id=request.data['id'])
		rq_u = self.request.user
		f = Favorite.objects.filter(Q(user=rq_u) & Q(movie=rq_m)).filter()
		if not f:
			f = Favorite()
			f.user = rq_u
			f.movie = rq_m
			f.save()
			return Response(HTTP_200_OK, status=status.HTTP_200_OK)
		else:
			return Response(HTTP_406_NOT_ACCEPTABLE, status=status.HTTP_406_NOT_ACCEPTABLE)

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
			return Response(HTTP_200_OK, status=status.HTTP_200_OK)
		return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)


class CinemaViewSet(viewsets.ModelViewSet):
	queryset = Cinema.objects.all()
	serializer_class = CinemaSerializer
	permission_classes = (IsAuthenticated | NotAuthenticatedCreateOnly, )
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]


class UserProfileViewSet(viewsets.ModelViewSet, generics.ListAPIView, ):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = (IsAuthenticated | NotAuthenticatedCreateOnly, )
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]

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

			return Response(HTTP_200_OK, status=status.HTTP_200_OK)
		return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)

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
				c = Cinema()
				c.owner = u
				c.name = formData['cinemaName']
				c.save()
				groups = [Group.objects.get(name='CinemaOwner')]
			u.groups.set(groups)
			u.save()

			p = UserProfile.objects.get(user=u)
			p.role = formData['role']
			p.save()

			return Response(HTTP_200_OK, status=status.HTTP_200_OK)
		return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated | NotAuthenticatedCreateOnly, )
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]