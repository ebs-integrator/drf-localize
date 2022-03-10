from django.apps import AppConfig

# Import your package here.

from drf_localize.core import (
    localize,
    localize_platform,
    localize_key_type
)


# Create your config here.

class DRFLocalizeConfig(AppConfig):
    name = 'drf_localize'
    verbose_name = "DRFLocalizeConfig"


default_app_config = 'drf_localize.DRFLocalizeConfig'
