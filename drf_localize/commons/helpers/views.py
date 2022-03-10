import inspect
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    BasePermissionMetaclass,
)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

# Import your package here.

from drf_localize.commons.permissions import IsLockedPermission
from drf_localize.settings import settings


# Create your views here.

class ExtendedViewSetPermissions(GenericViewSet):
    permission_classes_by_action = {
        'default': [AllowAny]
    }

    @staticmethod
    def make_permissions(classes: list = None):
        permissions = []

        if classes is None:
            classes = []

        if not isinstance(classes, list) and issubclass(type(classes), BasePermission):
            classes = [classes]

        for permission in classes:
            if issubclass(type(permission), BasePermission) or issubclass(type(permission), BasePermissionMetaclass):
                permissions.append(permission if not inspect.isclass(permission) else permission())  # noqa

        return permissions

    def get_permissions(self):
        permissions = self.make_permissions(classes=self.permission_classes)

        # Action is unknown return locked
        if not self.action:
            return self.make_permissions(classes=[IsLockedPermission])

        try:
            # Return permission_classes depending on `action`
            permissions = self.make_permissions(classes=self.permission_classes_by_action[self.action])
        except KeyError:
            # Action is not set return default permission_classes_by_action, if exists
            if default := self.permission_classes_by_action.get('default'):
                permissions = self.make_permissions(classes=default)

        return permissions


class ExtendedViewSet(ExtendedViewSetPermissions):
    http_method_names = ('get', 'post', 'patch', 'delete',)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = None
    serializer_class = None
    prefetch_related = ()
    select_related = ()
    filter_set_fields = ['id', ]
    search_fields = ['id', ]
    ordering_fields = ['id', ]
    ordering = ['-id', ]
    permission_classes_by_action = {
        'default': [AllowAny],
    }
    pagination_class = settings.PAGINATION_CLASS

    def get_prefetch_related(self):
        if isinstance(self.prefetch_related, str):
            return f'{self.prefetch_related}',

        if isinstance(self.prefetch_related, tuple):
            return self.prefetch_related
        return ()

    def get_select_related(self):
        if isinstance(self.select_related, str):
            return f'{self.select_related}',

        if isinstance(self.select_related, tuple):
            return self.select_related
        return ()

    def get_queryset_base(self):
        return self.queryset.model.objects

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return

        default_prefetch_related = self.get_prefetch_related()
        default_select_related = self.get_select_related()

        queryset = self.get_queryset_base().prefetch_related(
            *default_prefetch_related
        ).select_related(
            *default_select_related
        ).all()

        return queryset


class ExtendedListAPIView(
    ListAPIView,
    ExtendedViewSet
):
    pass


class ExtendedCreateAPIView(
    CreateAPIView,
    ExtendedViewSet
):
    pass


class ExtendedRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView,
    ExtendedViewSet
):
    pass


class BasicModelViewSet(
    ExtendedListAPIView,
    ExtendedCreateAPIView,
    ExtendedRetrieveUpdateDestroyAPIView,
    ExtendedViewSet
):
    pass
