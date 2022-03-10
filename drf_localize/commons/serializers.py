from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ChoiceField
)
from rest_framework.exceptions import ValidationError

# Import your package here.

from drf_localize.core import (
    localize_key_type
)
from drf_localize.models import (
    LocalizeKey,
    LocalizeLanguage
)
from drf_localize.serializers import (
    I18NModelSerializer
)


# Create your serializers here.


class LocalizeKeySerializer(I18NModelSerializer):
    code = CharField(required=True)
    type = ChoiceField(choices=localize_key_type.KEY_CHOICES, required=False, default=localize_key_type.KEY_PLAIN)

    class Meta:
        model = LocalizeKey
        fields = [
            'id',
            'code',
            'i18n',
            'type'
        ]

    @classmethod
    def unique_code(cls):
        raise ValidationError({'code': [_('This code already exists.')]})

    def validates_code(self, **kwargs):
        code = kwargs.get('code', '')
        typing = kwargs.get('type', localize_key_type.KEY_PLAIN)
        if LocalizeKey.objects.filter(code=code, type=typing).exists():
            self.unique_code()

    def create(self, validated_data):
        # Validate
        self.validates_code(**validated_data)

        try:
            instance = super(LocalizeKeySerializer, self).create(validated_data)
        except IntegrityError:
            self.unique_code()

        return instance  # noqa

    def update(self, instance, validated_data):
        # Validate
        self.validates_code(**validated_data)

        try:
            instance = super(LocalizeKeySerializer, self).update(instance, validated_data)
        except IntegrityError:
            self.unique_code()

        return instance


class LocalizeLanguageSerializer(ModelSerializer):
    class Meta:
        model = LocalizeLanguage
        fields = [
            'code',
            'name',
            'native'
        ]
