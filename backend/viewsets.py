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
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				startDate = self.request.query_params.get('startDate', None)
				if startDate is not None:
					queryset = Movie.objects.filter(Q(startDate__lte=startDate) & Q(endDate__gte=startDate))
				elif userInfo.roles[0].name == 'member':
					queryset = self.queryset
				elif userInfo.roles[0].name == 'owner':
					queryset = Movie.objects.filter(cinema__owner=userInfo.id)
				else:
					queryset = self.queryset
				if isinstance(queryset, QuerySet):
					# Ensure queryset is re-evaluated on each request.
					queryset = queryset.all()
				return queryset
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def list(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				my_param = request.query_params
				excl = []
				if userInfo.roles[0].name == 'member':
					excl = []
				elif userInfo.roles[0].name == 'owner':
					excl = ['cinema', 'availability']
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
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def create(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			token = self.request.headers['Authorization']
			response = getOwnInfo__request(token)
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				c = Cinema.objects.get(owner=userInfo.id)
				if c:
					movieInfo = request.data
					m = Movie()
					m.title = movieInfo['title']
					m.startDate = movieInfo['startDate']
					m.endDate = movieInfo['endDate']
					m.category = movieInfo['category']
					c = Cinema.objects.get(owner=userInfo.id)
					m.cinema = c
					m.availability = False
					m.save()
					# create orion entity
					entity = {
						"id": m.id.__str__(),
						"type": "Movie",
						"availability": {
							"value": 0,
							"type": "Integer"
						},
					}
					response = createEntity__request(entity, token)
					print("Movie entity CREATION: Status: {} and reason: {}".format(response.status, response.reason))
					# create orion subscription
					subscription = {
						"description": "Movie " + m.id.__str__() + " " + m.title + " Subscription",
						"subject": {
							"entities": [
								{
									"id": m.id.__str__(),
									"type": "Movie"
								}
							],
							"condition": {
								"attrs": [
									"availability"
								]
							}
						},
						"notification": {
							"attrsFormat": "keyValues",
							"http": {
								"url": "http://application:8000/api/Notification/"
							},
							"attrs": [
								"availability"
							]
						}
					}
					response = createSubscription__request(subscription, token)
					print("Movie subscription CREATION: Status: {} and reason: {}".format(response.status,
					                                                                      response.reason))
					return Response(HTTP_200_OK, status=status.HTTP_200_OK)
				return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def update(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			token = self.request.headers['Authorization']
			response = getOwnInfo__request(token)
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				m = Movie.objects.get(id=kwargs['pk'])
				c = Cinema.objects.get(owner=userInfo.id)
				if c:
					movieInfo = request.data
					m.title = movieInfo['title']
					m.startDate = movieInfo['startDate']
					m.endDate = movieInfo['endDate']
					m.category = movieInfo['category']
					m.availability = movieInfo['availability']
					c = Cinema.objects.get(owner=userInfo.id)
					m.cinema = c
					m.save()
					# update orion entity
					if m.availability:
						print('available')
						entity = {
							"availability": {
								"value": 1,
								"type": "Integer"
							},

						}
					elif not m.availability:
						print('not available')
						entity = {
							"availability": {
								"value": 0,
								"type": "Integer"
							},
						}
					response = updateEntity__request(m.id.__str__(), entity, token)
					print("Movie entity UPDATE: Status: {} and reason: {}".format(response.status, response.reason))
					return Response(HTTP_200_OK, status=status.HTTP_200_OK)
				return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def destroy(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			token = self.request.headers['Authorization']
			response = getOwnInfo__request(token)
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				movie = self.get_object()
				response = deleteEntity__request(movie.id.__str__(), token)
				subscription_id = Notifications.objects.get(movie__id=movie.id).subscription
				print("Movie entity DELETE: Status: {} and reason: {}".format(response.status, response.reason))
				response = deleteSubscription__request(subscription_id.__str__(), token)
				print("Movie subscription DELETE: Status: {} and reason: {}".format(response.status, response.reason))
				movie.delete()
				return Response(HTTP_200_OK, status=status.HTTP_200_OK)
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)


class FavoriteViewSet(viewsets.ModelViewSet):
	queryset = Favorite.objects.all()
	serializer_class = FavoriteSerializer
	permission_classes = (AllowAny,)
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]

	def list(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				my_param = request.query_params
				if userInfo.roles[0].name == 'member':
					if 'titleList' in my_param:
						f_titles = Favorite.objects.filter(user=userInfo.id).values_list('movie__title')
						dt = []
						for vr in f_titles:
							dt.append(vr[0])
						return Response({'title': dt})
				else:
					return Response(HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)
				self.serializer_class = FavoriteSerializer
				return super().list(request, *args, **kwargs)
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def get_queryset(self):
		assert self.queryset is not None, (
				"'%s' should either include a `queryset` attribute, "
				"or override the `get_queryset()` method."
				% self.__class__.__name__
		)
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				if userInfo.roles[0].name == 'member':
					queryset = Favorite.objects.filter(user=userInfo.id)
				else:
					queryset = self.queryset
				if isinstance(queryset, QuerySet):
					# Ensure queryset is re-evaluated on each request.
					queryset = queryset.all()
				return queryset
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def create(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				rq_m = Movie.objects.get(id=request.data['id'])
				rq_u = userInfo.id
				f = Favorite.objects.filter(Q(user=rq_u) & Q(movie=rq_m)).filter()
				if not f:
					f = Favorite()
					f.user = rq_u
					f.movie = rq_m
					f.save()
					return Response(HTTP_200_OK, status=status.HTTP_200_OK)
				else:
					return Response(HTTP_406_NOT_ACCEPTABLE, status=status.HTTP_406_NOT_ACCEPTABLE)
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)



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

	def get_queryset(self):
		assert self.queryset is not None, (
				"'%s' should either include a `queryset` attribute, "
				"or override the `get_queryset()` method."
				% self.__class__.__name__
		)
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				queryset = self.queryset
				if isinstance(queryset, QuerySet):
					# Ensure queryset is re-evaluated on each request.
					queryset = queryset.all()
				return queryset
			else:
				return Request.objects.none()
		else:
			return Request.objects.none()

	def list(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
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
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def update(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				if request.data['Type'] == 'update':
					formData = json.loads(request.data['formData'], object_hook=lambda d: SimpleNamespace(**d))
					r = Request.objects.get(id=kwargs['pk'])
					# if there is not user id in the request, there is no created user. Create one!
					if r.userId == '':
						# create a user in keyrock with the given credentials
						response = createUser__request(r, self.request.headers[adminTokenHeaderName])
						print("Create User: Status: {} and reason: {}".format(response.status, response.reason))
						# If success add role to the created user
						if is_success(response.status):
							data = response.read().decode("utf-8")
							parsed = json.loads(data)
							r = Request.objects.get(id=kwargs['pk'])
							r.userId = parsed['user']['id']
							r.password = ''
							r.is_active = True
							r.save()
							response = assignRole__request(r, self.request.headers[adminTokenHeaderName])
							print("Assign Role: Status: {} and reason: {}".format(response.status, response.reason))
						else:
							return Response(response, status=response.status)
					# if formData role is different from the existent change roles
					if r.role != formData.role:
						formData.userId = r.userId
						delResponse = deleteRole__request(r, self.request.headers[adminTokenHeaderName])
						print("Delete Role:Status: {} and reason: {}".format(delResponse.status, delResponse.reason))
						if is_success(delResponse.status):
							assResponse = assignRole__request(formData, self.request.headers[adminTokenHeaderName])
							print("Assign Role: Status: {} and reason: {}".format(assResponse.status,
							                                                      assResponse.reason))
							if not is_success(assResponse.status):
								assResponse = assignRole__request(r, self.request.headers[adminTokenHeaderName])
								print("Assign old Role: Status: {} and reason: {}".format(assResponse.status,
								                                                          assResponse.reason))
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
					if r.role == 'owner' and Cinema.objects.filter(owner=r.userId).count() == 0:
						cn = Cinema()
						cn.name = formData.cinema
						cn.owner = r.userId
						cn.save()
						r.cinema = formData.cinema
						r.save()
					elif r.role == 'owner' and Cinema.objects.filter(owner=r.userId).count() == 1:
						cn = Cinema.objects.get(owner=r.userId)
						cn.name = formData.cinema
						cn.owner = r.userId
						cn.save()
						r.cinema = formData.cinema
						r.save()
					return Response(HTTP_200_OK, status=status.HTTP_200_OK)
				else:
					return Response(HTTP_304_NOT_MODIFIED, status=status.HTTP_304_NOT_MODIFIED)
			else:
				return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def destroy(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				r = Request.objects.get(id=kwargs['pk'])
				if r.userId == '':
					r.delete()
				elif len(r.userId) > 1:
					response = deleteUser__request(r, self.request.headers[adminTokenHeaderName])
					print("Delete User: Status: {} and reason: {}".format(response.status, response.reason))
					if is_success(response.status):
						if r.role == 'member':
							fv = Favorite.objects.filter(user=r.userId)
							fv.delete()
							r = Request.objects.get(id=kwargs['pk'])
							r.delete()
						elif r.role == 'owner':
							cn = Cinema.objects.filter(owner=r.userId)
							cn.delete()
							r = Request.objects.get(userId=r.userId)
							r.delete()
					else:
						return Response(response, status=response.status)
			return Response(HTTP_200_OK)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def create(self, request, *args, **kwargs):
		if request.data['Type'] == 'Registration':
			formData = json.loads(request.data['formData'])
			r = Request()
			r.userId = ''
			r.userName = formData['surname'] + ' ' + formData['name']
			r.email = formData['email']
			r.password = formData['password']
			r.is_active = False
			r.role = formData['role']
			if formData['role'] == 'owner':
				r.cinema = formData['cinemaName']
			r.save()
			return Response(HTTP_200_OK, status=status.HTTP_200_OK)
		return Response(HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)


class NotificationsViewSet(viewsets.ModelViewSet):
	queryset = Notifications.objects.all()
	serializer_class = NotificationsSerializer
	permission_classes = (AllowAny,)
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]

	def create(self, request, *args, **kwargs):
		orionData = request.data
		subscriptionId = orionData['subscriptionId']
		subsData = orionData['data'][0]
		n_f = Notifications.objects.filter(subscription=subscriptionId)
		if not n_f:
			n_f = Notifications()
			n_f.subscription = subscriptionId
			n_f.movie = Movie.objects.get(id=subsData['id'])
			if subsData['availability'] == 0:
				n_f.notification = 'Η ταινία ' + n_f.movie.title + ' δεν είναι πλέον διαθέσιμη στον Κινηματογράφο ' + n_f.movie.cinema.name + '.'
			elif subsData['availability'] == 1:
				n_f.notification = 'Η ταινία ' + n_f.movie.title + ' είναι πλέον διαθέσιμη στον Κινηματογράφο ' + n_f.movie.cinema.name + '.'
		else:
			n_f = Notifications.objects.get(subscription=subscriptionId)
			if subsData['availability'] == 0:
				n_f.notification = 'Η ταινία ' + n_f.movie.title + ' δεν είναι πλέον διαθέσιμη στον Κινηματογράφο ' + n_f.movie.cinema.name + '.'
			elif subsData['availability'] == 1:
				n_f.notification = 'Η ταινία ' + n_f.movie.title + ' είναι πλέον διαθέσιμη στον Κινηματογράφο ' + n_f.movie.cinema.name + '.'
		n_f.save()
		# update seen filed for this subscription for every subscribed user
		UserSubscriptions.objects.filter(notification=n_f).update(seen=False)
		return Response(HTTP_200_OK, status=status.HTTP_200_OK)


class UserSubscriptionsViewSet(viewsets.ModelViewSet):
	queryset = UserSubscriptions.objects.all()
	serializer_class = UserSubscriptionsSerializer
	permission_classes = (AllowAny,)
	filter_backends = [filters.SearchFilter]
	search_fields = [filters.SearchFilter]

	def get_queryset(self):
		assert self.queryset is not None, (
				"'%s' should either include a `queryset` attribute, "
				"or override the `get_queryset()` method."
				% self.__class__.__name__
		)
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				if userInfo.roles[0].name == 'member':
					queryset = UserSubscriptions.objects.filter(user=userInfo.id)
				else:
					queryset = self.queryset
				if isinstance(queryset, QuerySet):
					# Ensure queryset is re-evaluated on each request.
					queryset = queryset.all()
				return queryset
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def update(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			token = self.request.headers['Authorization']
			response = getOwnInfo__request(token)
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				if request.data['Type'] == 'seen':
					UserSubscriptions.objects.filter(id=kwargs['pk']).update(seen=True)
				return Response(HTTP_200_OK, status=status.HTTP_200_OK)
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)


	def create(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			response = getOwnInfo__request(self.request.headers['Authorization'])
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				sb_m = Movie.objects.get(id=request.data['movie']['id'])
				print(sb_m)
				sb_u = userInfo.id
				new_sb = UserSubscriptions.objects.filter(Q(user=sb_u) & Q(notification__movie=sb_m)).filter()
				if not new_sb:
					new_sb = UserSubscriptions()
					new_sb.user = sb_u
					new_sb.notification = Notifications.objects.get(movie=sb_m)
					new_sb.seen = True
					new_sb.save()
					return Response(HTTP_200_OK, status=status.HTTP_200_OK)
				else:
					return Response(HTTP_406_NOT_ACCEPTABLE, status=status.HTTP_406_NOT_ACCEPTABLE)
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)

	def destroy(self, request, *args, **kwargs):
		if 'Authorization' in self.request.headers:
			token = self.request.headers['Authorization']
			response = getOwnInfo__request(token)
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				movie = Movie.objects.get(id=kwargs['pk'])
				usSub = UserSubscriptions.objects.get(Q(user=userInfo.id) & Q(notification__movie=movie))
				usSub.delete()
				return Response(HTTP_200_OK, status=status.HTTP_200_OK)
			else:
				return Response(response, status=response.status)
		else:
			return Response(HTTP_401_UNAUTHORIZED, status=status.HTTP_401_UNAUTHORIZED)
