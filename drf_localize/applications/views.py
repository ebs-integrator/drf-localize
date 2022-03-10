from drf_yasg import openapi
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# Import your package here.

from drf_localize.applications.permissions import (
    IsLocalizeApplicationSetPermission,
)
from drf_localize.applications.serializers import (
    LocalizeApplicationSerializer,
    LocalizeApplicationLanguageSerializer,
)
from drf_localize.commons.serializers import (
    LocalizeLanguageSerializer
)
from drf_localize.models import (
    LocalizeApplication
)
from drf_localize.commons.helpers.views import (
    ExtendedCreateAPIView
)

# Create your responses here.

application_response = openapi.Response('Localize application response, ', LocalizeApplicationSerializer)
languages_response = openapi.Response('Localize languages response, ', LocalizeLanguageSerializer(many=True))


# Create your views here.


class LocalizeApplicationsViewSet(ExtendedCreateAPIView):
    http_method_names = ('post',)
    queryset = LocalizeApplication.objects.all()
    serializer_class = LocalizeApplicationSerializer
    filter_set_fields = ['id', 'title', 'description', 'hash']
    search_fields = filter_set_fields
    ordering_fields = filter_set_fields


class LocalizeApplicationViewSet(ViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsLocalizeApplicationSetPermission],
            url_path='application',
            url_name='application')
    @swagger_auto_schema(responses={200: application_response})
    def application(self, request, *args, **kwargs):
        return Response(data=LocalizeApplicationSerializer(request.application).data)

    @application.mapping.patch
    @swagger_auto_schema(request_body=LocalizeApplicationSerializer, responses={200: application_response})
    def application_update(self, request, *args, **kwargs):
        instance = request.application
        serializer = LocalizeApplicationSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=LocalizeApplicationSerializer(instance).data)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsLocalizeApplicationSetPermission],
            url_path='application/languages',
            url_name='application_languages')
    @swagger_auto_schema(responses={200: languages_response})
    def application_languages(self, request, *args, **kwargs):
        languages = request.application.languages.all()
        return Response(data=LocalizeLanguageSerializer(languages, many=True).data)

    @application_languages.mapping.post
    @swagger_auto_schema(request_body=LocalizeApplicationLanguageSerializer, responses={200: languages_response})
    def application_languages_set(self, request, *args, **kwargs):
        serializer = LocalizeApplicationLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Languages reference
        languages_id = data.get('languages_id', [])
        request.application.languages.add(*languages_id)

        return Response(data=LocalizeLanguageSerializer(languages_id, many=True).data)

    @application_languages.mapping.delete
    @swagger_auto_schema(request_body=LocalizeApplicationLanguageSerializer, responses={200: languages_response})
    def application_languages_unset(self, request, *args, **kwargs):
        serializer = LocalizeApplicationLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Languages reference
        languages_id = data.get('languages_id', [])
        request.application.languages.remove(*languages_id)

        return Response(data=LocalizeLanguageSerializer(languages_id, many=True).data)
