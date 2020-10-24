from rest_framework.permissions import (DjangoModelPermissions, BasePermission)


class CustomDjangoModelPermissions(DjangoModelPermissions):
	"""Use this class in your viewsets to follow user group permissions (even GET requests)"""
	def __init__(self):
		self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class NotAuthenticatedCreateOnly(BasePermission):
	def has_permission(self, request, view):
		if request.method == 'POST' and request.user and not request.user.is_authenticated:
			return True
		return False
