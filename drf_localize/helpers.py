from django.utils.translation import ugettext_lazy as _


class LanguageHelper:
    LANGUAGE_RO = 'ro'
    LANGUAGE_EN = 'en'
    LANGUAGE_RU = 'ru'
    LANGUAGE_DE = 'de'

    CHOICES = (
        (LANGUAGE_RO, _('Romanian')),
        (LANGUAGE_EN, _('English')),
        (LANGUAGE_RU, _('Russian')),
        (LANGUAGE_DE, _('German')),
    )

    CODES = [LANGUAGE_EN, LANGUAGE_RU, LANGUAGE_RO, LANGUAGE_DE]
