from django.conf import settings as django_settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings as _APISettings

# Import your package here.

from drf_localize.commons.helpers import format_lazy
from drf_localize.commons.helpers.classes import LocalizeENUM

# Create your package settings here.

USER_SETTINGS = getattr(django_settings, 'DRF_LOCALIZE', None)

DEFAULTS = {
    'LANGUAGES': LocalizeENUM.ALL,
    'BASE_DIR': django_settings.BASE_DIR,
    'API_KEY_HEADER_NAME': 'HTTP_X_API_KEY',
    'PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'KEY_MODEL_CLASS': 'drf_localize.models.LocalizeKey',
    'LANGUAGE_MODEL_CLASS': 'drf_localize.models.LocalizeLanguage',
    'LANGUAGE_MODEL_CLASS_FIELD': 'code',
}

IMPORT_STRINGS = (
    'MIDDLEWARE_CLASS',
    'PAGINATION_CLASS',
    'KEY_MODEL_CLASS',
    'LANGUAGE_MODEL_CLASS'
)

REMOVED_SETTINGS = (
)


class APISettings(_APISettings):
    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "NONE"

        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    format_lazy(
                        _(
                            "The '{}' setting has been removed. Please refer to '{}' for available settings."
                        ),
                        setting,
                        SETTINGS_DOC,
                    )
                )

        return user_settings


settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_settings(*args, **kwargs):
    global settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'DRF_LOCALIZE':
        settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_settings)
