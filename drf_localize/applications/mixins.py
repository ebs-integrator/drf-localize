from django.db import models

# Import your package here.

from drf_localize.applications.managers import (
    ApplicationAwareManager,
    ApplicationUnawareManager
)


# Create your mixins here.

class ApplicationAwareModelMixin(models.Model):
    """
    An abstract base class model that provides a foreign key to an application
    """
    application = models.ForeignKey("LocalizeApplication", on_delete=models.CASCADE, null=True)

    objects = ApplicationAwareManager()
    ignored = ApplicationUnawareManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True
