from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from drf_localize_test.views import BlogViewSet

# Import your package here.

from drf_localize.urls import urlpatterns as localize_urlpatterns


# Create your helper functions here.


def schema_view_patterns(patterns=None):
    if patterns is None:
        patterns = []

    return get_schema_view(
        openapi.Info(
            title=f'API Documentation',
            default_version='v1',
            description=f'API'
        ),
        validators=['ssv'],
        public=True,
        patterns=patterns,
        permission_classes=(AllowAny,),
    )


# Create your patterns here.

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'blog', BlogViewSet, basename='blog')

urlpatterns = [
    *router.urls,
    path('', schema_view_patterns(patterns=localize_urlpatterns).with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

]

urlpatterns += localize_urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
