from django.utils.functional import SimpleLazyObject
from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import User


class PublicReadOnly(BasePermission):
	def has_permission(self, request, view):
		if type(request.user) in [SimpleLazyObject, User]:
			return True
		if request.method in SAFE_METHODS:
			return True
		return False