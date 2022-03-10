import json
import os
import shutil
import xml.etree.cElementTree as et
from time import time
from typing import Union
from django.db.models.base import ModelBase
from contextlib import suppress
from zipfile import ZipFile

# Import your package here.

from drf_localize.settings import settings
from drf_localize.commons.helpers import upsert_file
from drf_localize.commons.helpers.classes import LocalizeENUM


# Create your classes here.

class LocalizePlatform:
    PLATFORM_IOS = 'IOS'
    PLATFORM_ANDROID = 'ANDROID'
    PLATFORM_WEB = 'WEB'

    PLATFORM_TYPES = [PLATFORM_IOS, PLATFORM_ANDROID, PLATFORM_WEB]
    PLATFORM_CHOICES = (
        (PLATFORM_IOS, PLATFORM_IOS),
        (PLATFORM_ANDROID, PLATFORM_ANDROID),
        (PLATFORM_WEB, PLATFORM_WEB)
    )


localize_platform = LocalizePlatform()


class LocalizeKeyType:
    KEY_NAMESPACE = 'NAMESPACE'
    KEY_PLAIN = 'PLAIN'

    KEY_TYPES = [KEY_NAMESPACE, KEY_PLAIN]
    KEY_CHOICES = (
        (KEY_NAMESPACE, KEY_NAMESPACE),
        (KEY_PLAIN, KEY_PLAIN)
    )


localize_key_type = LocalizeKeyType()


class Localize:
    i18n: dict = {}
    key: str = ''
    namespace: str = ''
    codes: list = []
    mapping: dict = {}
    language: str = ''
    namespaces: list = []
    keys: list = []

    def __init__(self):
        self._methods()

    def _methods(self):
        """
        Attach dynamic methods to set language translation
        """

        def make_method(code=''):
            def wrapper(context, value=''):
                if not any([context.key, context.namespace]):
                    raise ValueError('Localize key or namespace is not set')

                # Check typing of value for key
                if context.key and not isinstance(value, str):
                    raise ValueError('Localize key value string type expected')

                # Check typing of value for namespace
                if context.namespace and not isinstance(value, dict):
                    raise ValueError('Localize namespace value dictionary type expected')

                # Set language code dict
                if namespace := context.namespace:
                    namespace = context.i18n.get(namespace, {})

                    for key, item in value.items():
                        if not isinstance(item, str):
                            continue

                        # Add language code key to namespace
                        if not namespace.get(code, None):
                            namespace.update({code: {}})

                        # Set language code key - value
                        namespace[code].update({key: item})

                # Set language code value
                if key := context.key:
                    context.i18n.get(key, {}).update({code: value})

                return context

            return wrapper

        # Attach dynamic methods
        for language in self.languages():
            setattr(Localize, f'set_{language}', make_method(code=language))

    def languages(self, source: str = '../fixtures/localizelanguages.json') -> list:
        """
        Set language keys
        """
        if self.codes:
            return self.codes

        path = os.path.abspath(os.path.dirname(__file__))
        file = open(f'{os.path.join(path, source)}')
        objects = json.load(file)

        for element in objects:
            fields = element.get('fields', {})
            self.codes.append(fields.get('code', ''))

        return list(set(self.codes))

    @staticmethod
    def get_languages(request=None) -> list:
        """
        Get languages from request application or settings or model
        """
        field = settings.LANGUAGE_MODEL_CLASS_FIELD
        application = getattr(request, 'application', None)
        localize_languages = []
        application_languages = list(application.languages.values_list(field, flat=True)) if application else []
        model = settings.LANGUAGE_MODEL_CLASS

        if (not application_languages) and issubclass(type(model), ModelBase):
            # Ignore any exception from invalid model
            with suppress(Exception):
                localize_languages = list(
                    model.objects.values_list(field, flat=True))  # noqa

        # Application languages has higher priority
        service_languages = settings.LANGUAGES
        if service_languages == LocalizeENUM.ALL:
            return application_languages or localize_languages

        return list(set(localize_languages).intersection(service_languages))

    def set_key(self, name: str = ''):
        if not isinstance(name, str):
            raise ValueError('Localize key name string type expected')

        self.i18n.update({name: {}})
        self.key = name
        self.namespace = ''
        self.keys.append(name)
        return self

    def set_key_namespace(self, name: str = ''):
        if not isinstance(name, str):
            raise ValueError('Localize namespace name string type expected')

        self.i18n.update({name: {}})
        self.namespace = name
        self.key = ''
        self.namespaces.append(name)
        return self

    def reset(self):
        self.key = ''
        self.namespace = ''
        return self

    def reset_key(self):
        self.key = ''
        return self

    def reset_namespace(self):
        self.namespace = ''
        return self

    def get_i18n(self) -> dict:
        return self.i18n

    def get_key(self) -> str:
        return self.key

    def get_namespace(self) -> str:
        return self.namespace

    def build_keys(self, language: str = ''):
        if language not in self.codes:
            raise ValueError('Unknown localize language')

        self.mapping = {}
        for code, i18n in self.i18n.items():
            if not isinstance(i18n, dict):
                continue

            for key, value in i18n.items():
                if key != language or not isinstance(value, str):
                    continue
                self.mapping.update({code: value})

        self.language = language
        return self

    def build_keys_namespace(self, namespace: str = '', language: str = ''):
        if namespace not in self.namespaces:
            raise ValueError('Unknown localize namespace')

        if language not in self.codes:
            raise ValueError('Unknown localize language')

        self.mapping = {}
        for code, i18n in self.i18n.items():
            if not isinstance(i18n, dict) or code != namespace:
                continue

            keyed = i18n.get(language, {})
            if not isinstance(keyed, dict):
                continue

            for key, value in keyed.items():
                self.mapping.update({key: value})

        self.language = language
        return self

    def build(self, language: str = ''):
        if language not in self.codes:
            raise ValueError('Unknown localize language')

        self.mapping = {}
        mapping = {}

        # Building namespaces
        for namespace in self.namespaces:
            mapping.update(**self.build_keys_namespace(namespace=namespace, language=language).mapping)

        # Building keys
        mapping.update(**self.build_keys(language=language).mapping)

        self.mapping = mapping
        self.language = language
        return self

    @staticmethod
    def _make_language(language, mapping=None):
        if mapping is None:
            mapping = {}
        # Add language code key to mapping
        if not mapping.get(language, None):
            mapping.update({language: {}})
        return mapping

    @staticmethod
    def _make_zip(filename='', files=None):
        if files is None:
            files = []

        filename = f'{filename}.zip'
        zip_object = ZipFile(filename, 'w')

        for file in files:
            zip_object.write(file)

            if (path := os.path.dirname(file)) != '':
                shutil.rmtree(path)
            else:
                os.remove(file)

        zip_object.close()
        return filename

    def build_zip(self, request=None, platform: str = None) -> Union[str, list]:
        if platform and platform not in localize_platform.PLATFORM_TYPES:
            raise ValueError('Unknown localize platform')

        self.mapping = {}
        mapping = {}
        sources = {'namespaces': {}, 'keys': {}}
        languages = self.get_languages(request=request)

        # Build mapper for each language
        for language in languages:
            sources['keys'].update({
                language: self.build_keys(language=language).mapping
            })

            for namespace in self.namespaces:
                # Add namespace code key to namespace
                if not sources['namespaces'].get(namespace, None):
                    sources['namespaces'].update({namespace: {}})

                sources['namespaces'][namespace].update({
                    language: self.build_keys_namespace(namespace=namespace, language=language).mapping
                })

        # Building
        strings = []
        jsons = []
        xml = []

        for language, keys in sources['keys'].items():
            self._make_language(language=language, mapping=mapping)
            mapping[language].update(**keys)

        for namespace, source in sources['namespaces'].items():
            for language, keys in source.items():
                self._make_language(language=language, mapping=mapping)
                mapping[language].update(**keys)

        for language, keys in mapping.items():
            if not platform or platform == localize_platform.PLATFORM_IOS:
                strings.append(self.to_strings(filename=f'{language}.lproj/Localizable', mapping=keys))
            if not platform or platform == localize_platform.PLATFORM_WEB:
                jsons.append(self.to_json(filename=f'{language}/locales', mapping=keys))
            if not platform or platform == localize_platform.PLATFORM_ANDROID:
                xml.append(self.to_xml(filename=f'values-{language}/strings', mapping=keys))

        # Zip objects
        zips = []
        if not platform or platform == localize_platform.PLATFORM_ANDROID:
            zips.append(self._make_zip('strings', files=xml))
        if not platform or platform == localize_platform.PLATFORM_IOS:
            zips.append(self._make_zip('Localizable', files=strings))
        if not platform or platform == localize_platform.PLATFORM_WEB:
            zips.append(self._make_zip('locales', files=jsons))

        if not platform:
            zips = self._make_zip(str(int(time())), files=zips)

        if platform and zips:
            zips = next(iter(zips))

        return zips

    def to_xml(self, filename: str = 'keys', mapping: dict = None) -> str:
        if mapping is None:
            mapping = {}

        def _pretty_print(current, parent=None, index: int = -1, depth: int = 0):
            for i, node in enumerate(current):
                _pretty_print(node, current, i, depth + 1)

            if parent is not None:
                if index == 0:
                    parent.text = '\n' + ('\t' * depth)
                else:
                    parent[index - 1].tail = '\n' + ('\t' * depth)
                if index == len(parent) - 1:
                    current.tail = '\n' + ('\t' * (depth - 1))

        filename = f'{filename}.xml'
        upsert_file(filename)
        root = et.Element('resources')
        source = self.mapping.items() if not mapping else mapping.items()
        for code, translate in source:
            doc = et.SubElement(root, "string")
            doc.attrib['name'] = code
            doc.text = translate or " "

        _pretty_print(root)  # noqa
        tree = et.ElementTree(root)
        tree.write(filename, encoding='UTF-8', xml_declaration=True)
        return filename

    def to_json(self, filename: str = 'keys', mapping: dict = None) -> str:
        if mapping is None:
            mapping = {}

        source = self.mapping if not mapping else mapping
        lines = json.dumps(source, indent=4, sort_keys=True)

        filename = f'{filename}.json'
        upsert_file(filename)
        with open(filename, 'w') as f:
            f.write(lines)
        return filename

    def to_strings(self, filename: str = 'keys', mapping: dict = None) -> str:
        if mapping is None:
            mapping = {}

        lines = []
        source = self.mapping.items() if not mapping else mapping.items()
        for code, translate in source:
            line = f'"{code}" = "{translate}";'
            lines.append(line)

        filename = f'{filename}.strings'
        upsert_file(filename)
        with open(filename, 'w') as f:
            f.write('\n'.join(lines))

        return filename

    def to_platform(self, platform: str = '', filename: str = 'keys') -> str:
        if platform not in localize_platform.PLATFORM_TYPES:
            raise ValueError('Unknown localize platform')

        if platform == localize_platform.PLATFORM_ANDROID:
            return self.to_xml(filename=filename)

        if platform == localize_platform.PLATFORM_IOS:
            return self.to_strings(filename=filename)

        return self.to_json(filename=filename)

    def get_keys(self, request=None):
        model = settings.KEY_MODEL_CLASS
        translations = model.objects.values_list('code', 'i18n', 'type')

        for code, i18n, typing in translations:
            key = localize.set_key(code)

            if typing == localize_key_type.KEY_NAMESPACE:
                key = localize.set_key_namespace(code)

            for language in localize.get_languages(request=request):
                value = i18n.get(language, '')
                getattr(key, f'set_{language}')(value)

        return self


# Export localize instance
localize = Localize()
