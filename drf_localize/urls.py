from rest_framework import routers

# Import your package here.

from drf_localize.commons.views import (
    LocalizationKeyViewSet,
    LocalizationLanguageViewSet,
)

from drf_localize.applications.views import (
    LocalizeApplicationsViewSet,
    LocalizeApplicationViewSet,
)

# Create your patterns here.

router = routers.SimpleRouter(trailing_slash=False)

# Localize applications
router.register(r'localize/applications', LocalizeApplicationsViewSet, basename='localize-applications')
router.register(r'localize', LocalizeApplicationViewSet, basename='localize-application')

# Localize keys & languages
router.register(r'localize/keys', LocalizationKeyViewSet, basename='localize-keys')
router.register(r'localize/languages', LocalizationLanguageViewSet, basename='localize-languages')

# Create your patterns here.

urlpatterns = router.urls
