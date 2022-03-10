from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import (
    Serializer,
    JSONField,
    ModelSerializer,
)
from rest_framework.utils.serializer_helpers import BindingDict
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from django.db import models
from django.utils.functional import cached_property

# Import your package here.

from drf_localize.settings import settings
from drf_localize.core import (
    localize,
    localize_key_type
)


# Create your serializers here.


class I18N(Serializer):
    context: dict = None
    localize_namespace: bool = False
    localize_model: models.Model = None
    localize_translate: list = []

    def __init__(self, **kwargs):
        self.localize_model = kwargs.pop('model', None)
        self.context = kwargs.pop('context', None)
        self.localize_namespace = kwargs.pop('namespace', False)
        self.localize_translate = getattr(self.localize_model, 'LOCALIZE_TRANSLATE', [])
        self.localize_field = getattr(self.localize_model, 'LOCALIZE_FIELD', None)
        super(I18N, self).__init__(**kwargs)

    def to_representation(self, instance):
        # Not evaluating non-request context
        if 'request' not in self.context:
            return {}

        response = {}
        request = self.context.get('request', {})
        data = getattr(request, 'data', {})
        i18n = data.get(self.localize_field, {})
        languages = localize.get_languages(request=request)

        # Update i18n with request's language -> i18n.LANGUAGE_CODE -> i18n.en
        if language := request.LANGUAGE_CODE:
            response[language] = {}

        # Take i18n field from request body
        if i18n and isinstance(i18n, dict):
            keys = list(i18n.keys())

            # Check if i18n object has valid language keys
            if difference := list(set(keys) - set(languages)):
                raise ValidationError({
                    self.localize_field: [_('Unknown language keys "%(key)s".') % {'key': ','.join(difference)}]
                })

        # Attach language keys with values
        for language in languages:
            response[language] = {}
            value = i18n.get(language, '')
            value_string = value if isinstance(value, str) else ''

            # Model based field translation
            if self.localize_model and self.localize_translate:
                for field in self.localize_translate:
                    keyed_data = data.get(field, '')
                    keyed = i18n.get(language, {})
                    if not isinstance(keyed, dict):
                        keyed = {}

                    # Retrieve language field value, if set
                    keyed = keyed.get(field, '')
                    value_string = keyed if keyed and isinstance(keyed, str) else ''

                    # Defaulting to internal body key value
                    value_string = keyed_data if not value_string else value_string

                    # Update language code key value
                    response[language].update({field: value_string})

                # We are skipping the rest, because model based translation is already in use
                continue

            # Blank string if value is not string, and non-model
            response[language] = value_string

            # Namespacing keys, means each language is allowed to have 2nd level keys, non-model
            if self.localize_namespace:
                response[language] = {}
                if not isinstance(value, dict):
                    continue

                for key, value in value.items():
                    # Skipping if value is not string
                    if not isinstance(value, str):
                        continue

                    # Attach 2nd level value
                    response[language].update({key: value})

        return response

    def to_internal_value(self, data):
        return {self.localize_field: data}

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class I18NModelSerializer(ModelSerializer):

    def __init__(self, instance=None, data=empty, **kwargs):
        self.localize_model = self.Meta.model  # noqa
        self.localize_field = getattr(self.localize_model, 'LOCALIZE_FIELD', None)
        super(I18NModelSerializer, self).__init__(instance=instance, data=data, **kwargs)

    @cached_property
    def fields(self):
        """
        A dictionary of {field_name: field_instance}.
        """
        # `fields` is evaluated lazily. We do this to ensure that we don't
        # have issues importing modules that use ModelSerializers as fields,
        # even if Django's app-loading stage has not yet run.
        fields = BindingDict(self)
        for key, value in self.get_fields().items():
            fields[key] = value

        if self.localize_field:
            fields.update({
                self.localize_field: JSONField(
                    required=False, default={}
                )
            })
        return fields

    def _i18n(self, validated_data):
        typing = validated_data.get('type', None)
        serializer = I18N(
            data=self,
            context=self.context,
            model=self.localize_model,
            namespace=typing == localize_key_type.KEY_NAMESPACE
        )
        serializer.is_valid(raise_exception=True)

        # In case model does not have i18n field
        if self.localize_field:
            validated_data.update({self.localize_field: serializer.data})

        return validated_data

    def create(self, validated_data):
        validated_data = self._i18n(validated_data)
        return super(I18NModelSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._i18n(validated_data)
        return super(I18NModelSerializer, self).update(instance, validated_data)
