from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.http import (
    Http404,
    FileResponse
)

# Import your package here.

from drf_localize.commons.helpers.views import (
    ExtendedListAPIView,
    BasicModelViewSet
)
from drf_localize.core import (
    localize,
    localize_platform,
)
from drf_localize.commons.serializers import (
    LocalizeKeySerializer,
    LocalizeLanguageSerializer
)
from drf_localize.models import (
    LocalizeKey,
    LocalizeLanguage
)


# Create your views here.

class LocalizationLanguageViewSet(ExtendedListAPIView):
    http_method_names = ('get',)
    queryset = LocalizeLanguage.objects.all()
    serializer_class = LocalizeLanguageSerializer
    filter_set_fields = ['id', 'code', 'name', 'native']
    search_fields = filter_set_fields
    ordering_fields = filter_set_fields


class LocalizationKeyViewSet(BasicModelViewSet):
    queryset = LocalizeKey.objects.all()
    serializer_class = LocalizeKeySerializer
    filter_set_fields = ['id', 'code', 'type']
    search_fields = filter_set_fields
    ordering_fields = filter_set_fields

    @action(detail=False,
            methods=['GET'],
            url_path='(?P<platform>.+)/(?P<language>.+)/file',
            url_name='file')
    @swagger_auto_schema()
    def file(self, request, *args, **kwargs):
        platform = kwargs.get('platform', '').upper()
        language = kwargs.get('language', '').lower()

        if (language not in localize.codes) or (platform not in localize_platform.PLATFORM_TYPES):
            raise Http404()

        instance = localize.get_keys(request=request).build(language=language)
        file = instance.to_platform(platform=platform)
        return FileResponse(open(file, 'rb'), content_type='application/force-download')

    @action(detail=False,
            methods=['GET'],
            url_path='(?P<platform>.+)/zip',
            url_name='file')
    @swagger_auto_schema()
    def file_zip(self, request, *args, **kwargs):
        platform = kwargs.get('platform', '').upper()

        if platform not in localize_platform.PLATFORM_TYPES:
            raise Http404()

        zips = localize.get_keys(request=request).build_zip(request=request, platform=platform)
        return FileResponse(open(zips, 'rb'), content_type='application/force-download')

    @action(detail=False,
            methods=['GET'],
            url_path='zip',
            url_name='file')
    @swagger_auto_schema()
    def zip(self, request, *args, **kwargs):
        zips = localize.get_keys(request=request).build_zip(request=request)
        return FileResponse(open(zips, 'rb'), content_type='application/force-download')
