from rest_framework.permissions import BasePermission


# Create your permission classes here.

class IsLocalizeApplicationSetPermission(BasePermission):

    def has_permission(self, request, view):
        application = getattr(request, 'application', None)
        return application is not None
