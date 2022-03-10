from drf_localize.commons.errors import LockedError
from rest_framework.permissions import BasePermission


# Create your permission classes here.

class IsLockedPermission(BasePermission):

    def has_permission(self, request, view):
        raise LockedError()
