import json
from types import SimpleNamespace

from rest_framework.permissions import (DjangoModelPermissions, BasePermission)
from rest_framework.status import is_success
from backend.httpRequests import getOwnInfo__request


class CustomDjangoModelPermissions(DjangoModelPermissions):
	"""Use this class in your viewsets to follow user group permissions (even GET requests)"""
	def __init__(self):
		self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class NotAuthenticatedCreateOnly(BasePermission):
	def has_permission(self, request, view):
		if request.method == 'POST' and request.user and not request.user.is_authenticated:
			return True
		return False

class IsAuthenticated(BasePermission):
	def has_permission(self, request, view):
		if 'Authorization' in request.headers:
			token = request.headers['Authorization']
			response = getOwnInfo__request(token)
			print("Authorization: Status: {} and reason: {}".format(response.status, response.reason))
			if is_success(response.status):
				data = response.read().decode("utf-8")
				userInfo = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
				request.userInfo = userInfo
				request.auth = token
				return True
		return False

class AllowAny(BasePermission):
	def has_permission(self, request, view):
		request.userInfo = 'admin'
		return True