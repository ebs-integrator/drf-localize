import uuid
from django.db import models

# Import your package here.

from drf_localize.settings import settings
from drf_localize.applications.mixins import ApplicationAwareModelMixin
from drf_localize.core import LocalizeKeyType


# Create your functions here.

def hasher():
    return str(uuid.uuid4())


# Create your models here.


class LocalizeLanguage(models.Model):
    code = models.CharField(unique=True, max_length=2)
    name = models.CharField(max_length=128, null=True)
    native = models.CharField(max_length=128, null=True)


class LocalizeKey(ApplicationAwareModelMixin):
    LOCALIZE_FIELD = 'i18n'

    code = models.CharField(max_length=512)
    i18n = models.JSONField(default=dict)
    type = models.CharField(
        max_length=32,
        choices=LocalizeKeyType.KEY_CHOICES,
        default=LocalizeKeyType.KEY_PLAIN,
        db_index=True
    )

    class Meta:
        unique_together = ('code', 'application_id', 'type',)


class LocalizeApplication(models.Model):
    hash = models.CharField(max_length=254, editable=False, default=hasher, unique=True)
    title = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=254, null=True)
    languages = models.ManyToManyField(settings.LANGUAGE_MODEL_CLASS, default=list,
                                       through='LocalizeApplicationLanguage',
                                       related_name='applications')


class LocalizeApplicationLanguage(models.Model):
    application = models.ForeignKey(LocalizeApplication, on_delete=models.CASCADE)
    language = models.ForeignKey(settings.LANGUAGE_MODEL_CLASS, on_delete=models.CASCADE)
