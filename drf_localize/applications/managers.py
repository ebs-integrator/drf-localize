from django.db import models
from contextlib import suppress

# Import your package here.

from drf_localize.applications.helpers import (
    current_localize_application_id,
    current_localize_application
)


# Create your helper functions here.

def field_exists(model, field=''):
    with suppress(Exception):
        exists = model._meta.get_field(field)  # noqa
        return exists

    return False


# Create your managers here.

class ApplicationUnawareManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(application_id=None)


class ApplicationAwareManager(models.Manager):

    def get_queryset(self):
        # Injecting application_id filters in the get_queryset.
        # Injects application_id filter on the current model for all the non-join/join queries.
        application_id = current_localize_application_id()

        if not application_id:
            return self._queryset_class(self.model)

        filtering = {}
        if field_exists(self.model, 'application_id'):  # noqa
            filtering.update({'application_id': application_id})

        # If the manager was built from a queryset using
        # SomeQuerySet.as_manager() or SomeManager.from_queryset(),
        # we want to use that queryset instead of ApplicationAwareQuerySet.
        if self._queryset_class != models.QuerySet:
            return super().get_queryset().filter(**filtering)

        return ApplicationAwareQuerySet(self.model, using=self._db).filter(**filtering)


class ApplicationAwareQuerySet(models.QuerySet):

    @property
    def application(self):
        return current_localize_application()

    def create(self, **kwargs):
        application_id = current_localize_application_id()

        field = field_exists(self.model, 'application_id')
        if application_id and not (kwargs.get('application_id', None) or kwargs.get('application', None)) and field:
            kwargs.update({'application_id': application_id})

        return super().create(**kwargs)

    def update_or_create(self, defaults=None, **kwargs):
        application_id = current_localize_application_id()

        field = field_exists(self.model, 'application_id')
        if application_id and not (kwargs.get('application_id', None) or kwargs.get('application', None)) and field:
            kwargs.update({'application_id': application_id})

        return super().update_or_create(defaults=defaults, **kwargs)

    def get_or_create(self, defaults=None, **kwargs):
        application_id = current_localize_application_id()

        field = field_exists(self.model, 'application_id')
        if application_id and not (kwargs.get('application_id', None) or kwargs.get('application', None)) and field:
            kwargs.update({'application_id': application_id})

        return super().get_or_create(defaults=defaults, **kwargs)

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        application_id = current_localize_application_id()

        objs = list(objs)
        for obj in objs:
            field = field_exists(self.model, 'application_id')
            if field and not (obj.application_id or obj.application):
                obj.application_id = application_id

        return super().bulk_create(objs, batch_size, ignore_conflicts)

    def as_manager(cls):
        manager = ApplicationAwareManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True

    as_manager = classmethod(as_manager)
