import json
from types import SimpleNamespace
from django.db.models import Q, QuerySet

from backend.httpRequests import *
from backend.serializers import *

from rest_framework import filters, status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import AllowAny


class MovieViewSet(viewsets.ModelViewSet):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializer
	permission_classes = (AllowAny,)
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'category', 'cinema__name', 'startDate']

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
			queryset = Movie.objects.filter(Q(startDate__lte=startDate) & Q(endDate__gte=startDate))
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
	permission_classes = (AllowAny,)
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
	permission_classes = (AllowAny,)
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]


class RequestViewSet(viewsets.ModelViewSet):
	queryset = Request.objects.all()
	serializer_class = RequestSerializer
	permission_classes = (AllowAny,)
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]

	def list(self, request, *args, **kwargs):
		my_param = request.query_params
		if 'fields' in my_param:
			dt = []
			for vr in list(RequestSerializer.Meta.fields):
				dt.append(vr)
			return Response({'fields': dt})
		if self.request.user.is_superuser:
			self.serializer_class = RequestSerializer
		else:
			self.serializer_class = RequestSerializer
		return super().list(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		print(request.data['Type'])
		if request.data['Type'] == 'update':
			formData = json.loads(request.data['formData'], object_hook=lambda d: SimpleNamespace(**d))
			r = Request.objects.get(id=kwargs['pk'])
			# if there is not user id in the request, there is no created user. Create one!
			if r.userId == '':
				# create a user in keyrock with the given credentials
				response = createUser__request(r, self.request.headers[adminTokenHeaderName])
				# If success add role to the created user
				if is_success(response.status):
					data = response.read().decode("utf-8")
					parsed = json.loads(data)
					r = Request.objects.get(id=kwargs['pk'])
					r.userId = parsed['user']['id']
					r.password = ''
					r.save()
					assignRole__request(r, self.request.headers[adminTokenHeaderName])
				else:
					return Response(response, status=response.status)
			# if formData role is different from the existent change roles
			if r.role != formData.role:
				formData.userId = r.userId
				delResponse = deleteRole__request(r, self.request.headers[adminTokenHeaderName])
				print("Status: {} and reason: {}".format(delResponse.status, delResponse.reason))
				if is_success(delResponse.status):
					assResponse = assignRole__request(formData, self.request.headers[adminTokenHeaderName])
					if not is_success(assResponse.status):
						print('here')
						assResponse = assignRole__request(r, self.request.headers[adminTokenHeaderName])
						print("Status: {} and reason: {}".format(assResponse.status, assResponse.reason))
						return Response(HTTP_304_NOT_MODIFIED, status=status.HTTP_304_NOT_MODIFIED)
					else:

						r.role = formData.role
						r.save()
						if r.role == 'member':
							cn = Cinema.objects.get(owner=r.userId)
							cn.delete()
							r = Request.objects.get(id=kwargs['pk'])
							r.cinema = ''
							r.save()
				else:
					return Response(HTTP_304_NOT_MODIFIED, status=status.HTTP_304_NOT_MODIFIED)
			#  After changing role check if r.role='owner' and if there is existent cinema with the given name. If not create one.
			if r.role == 'owner' and Cinema.objects.filter(owner=r.userId).count() == 0 :
				cn = Cinema()
				cn.name = formData.cinema
				cn.owner = r.userId
				cn.save()
				r.cinema = formData.cinema
				r.save()
			elif r.role == 'owner' and Cinema.objects.filter(owner=r.userId).count() == 1 :
				cn = Cinema.objects.get(owner=r.userId)
				cn.name = formData.cinema
				cn.owner = r.userId
				cn.save()
				r.cinema = formData.cinema
				r.save()
			return  Response(HTTP_200_OK, status=status.HTTP_200_OK)
		else:
			return Response(HTTP_304_NOT_MODIFIED, status=status.HTTP_304_NOT_MODIFIED)


	def destroy(self, request, *args, **kwargs):
		r = Request.objects.get(id=kwargs['pk'])
		response = deleteUser__request(r, self.request.headers[adminTokenHeaderName])
		if is_success(response.status):
			cn = Cinema.objects.get(owner=r.userId)
			cn.delete()
			r = Request.objects.get(userId=r.userId)
			r.delete()
			print("\n\n\nStatus: {} and reason: {}".format(response.status, response.reason))
		return Response(response, status=response.status)

	def create(self, request, *args, **kwargs):
		import json
		if request.data['Type'] == 'Registration':
			formData = json.loads(request.data['formData'])
			r = Request()
			r.userId = ''
			r.userName = formData['surname'] + ' ' + formData['name']
			r.email = formData['email']
			r.password = formData['password']
			r.enabled =  False
			r.role = formData['role']
			if formData['role'] == 'owner':
				r.cinema = formData['cinemaName']
			r.save()
			return Response(HTTP_200_OK, status=status.HTTP_200_OK)
		return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)
