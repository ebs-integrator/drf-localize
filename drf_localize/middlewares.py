from django.utils.deprecation import MiddlewareMixin

# Import your package here.

from drf_localize.settings import settings
from drf_localize.models import (
    LocalizeApplication,
)
from drf_localize.applications.helpers import (
    set_current_localize_application,
)


# Create your middleware classes here.


class LocalizeApplicationMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        key = request.META.get(settings.API_KEY_HEADER_NAME)
        application = LocalizeApplication.objects.prefetch_related('languages').filter(hash=key).first()

        # Setting in thread
        request.application = application
        set_current_localize_application(application)
