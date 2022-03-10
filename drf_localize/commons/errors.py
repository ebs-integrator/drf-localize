from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _
from rest_framework.status import HTTP_423_LOCKED


# Create your errors here.

class LockedError(APIException):
    status_code = HTTP_423_LOCKED
    default_detail = _('You do not have permission to perform this action.')
    default_code = 'permission_denied'
