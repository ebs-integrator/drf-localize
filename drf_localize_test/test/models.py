from django.db import models


# Create your models here.

class Blog(models.Model):  # noqa

    # DRF Localize model specific constant, which is used to translate model fields
    LOCALIZE_TRANSLATE = ['title', 'description']  # or LOCALIZE_TRANSLATE = ['title', 'description']

    # DRF Localize model specific constant, which is used to store translations (json)
    LOCALIZE_FIELD = 'i18n'

    # DRF Localize model specific constant, which is used to auto-update or remove translations for new languages
    LOCALIZE_AUTO_UPDATE = True

    # Your custom model fields
    title = models.CharField(max_length=254, null=True)
    description = models.CharField(max_length=512, null=True)

    # Referenced json field to store translations
    i18n = models.JSONField(default=dict)
