# 🌐 DRF Localize

Package to provide localization experiences for mobile and api applications.

# ⚡️ Features

✅ Localize keys for multiple languages<br/>
✅ Generate localizable `iOS` , `Android`, `Web` compatible **zip** & **files**<br/>
✅ Model `JSON` based fields localization<br/>
✅ Library for localizable keys<br/>
✅ REST API for localizable keys<br/>
✅ Configurable

# 🔐 Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install drf_localize.

```bash
pip install drf_localize
```

then add it to your installed apps:

```python
INSTALLED_APPS = [
    ...,
    'drf_localize',
    ...,
]
```

then run migrate:

```bash
python manage.py migrate
```

and load initial data:

```bash
python manage.py loaddata localizelanguages
python manage.py loaddata localizekeys (optional)
```

# 🔨 Configuration

Configuration for **DRF Localize** is namespaced in a single django setting, named `DRF_LOCALIZE`, by default everything is configured out of the box.

```python
DRF_LOCALIZE = {
    'LANGUAGES': 'ALL',  # noqa
    'BASE_DIR': BASE_DIR,  # noqa
    'API_KEY_HEADER_NAME': 'HTTP_X_API_KEY',
    'PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'KEY_MODEL_CLASS': 'drf_localize.models.LocalizeKey',
    'LANGUAGE_MODEL_CLASS': 'drf_localize.models.LocalizeLanguage',
    'LANGUAGE_MODEL_CLASS_FIELD': 'code',
}
```

# 🔎 Available Settings

| Header                       | Description                                                           | Default                                         |
|:-----------------------------|:----------------------------------------------------------------------|:------------------------------------------------|
| `LANGUAGES`                  | **Specify language codes to use as array**.                           | ALL                                             |
| `BASE_DIR`                   | **Specify internal directory path**.                                  | BASE_DIR                                        |
| `API_KEY_HEADER_NAME`        | **Specify `X-API-Key` header**.                                       | HTTP_X_API_KEY                                  |
| `PAGINATION_CLASS`           | **Specify pagination class**.                                         | rest_framework.pagination.PageNumberPagination  |
| `KEY_MODEL_CLASS`            | **Specify key model class, must comply to `drf_localize` key model**. | drf_localize.models.LocalizeKey                 |
| `LANGUAGE_MODEL_CLASS`       | **Specify language model class**.                                     | drf_localize.models.LocalizeLanguage            |
| `LANGUAGE_MODEL_CLASS_FIELD` | **Specify language model class code field**.                          | code                                            |

# 🔧 Usage

Specify `localize` fields in your model

```python
from django.db import models


class Blog(models.Model):  # noqa

    # DRF Localize model specific constant, which is used to translate model fields
    LOCALIZE_TRANSLATE = ['title']  # or LOCALIZE_TRANSLATE = ['title', 'description']

    # DRF Localize model specific constant, which is used to store translations (json)
    LOCALIZE_FIELD = 'i18n'
    
    # DRF Localize model specific constant, which is used to auto-update or remove translations for languages
    LOCALIZE_AUTO_UPDATE = False # not required , defaults to False

    # Your custom model fields
    title = models.CharField(max_length=254, null=True)
    description = models.CharField(max_length=512, null=True)

    # Referenced json field to store translations
    i18n = models.JSONField(default=dict)
```

Inherit `I18NModelSerializer` in your model serializer

```python
from apps.blog.models import Blog  # noqa
from drf_localize.serializers import (
    I18NModelSerializer
)


class BlogSerializer(I18NModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

```

Use your model serializer in your endpoints as usual

```python
from apps.blog.models import Blog  # noqa
from apps.blog.serializers import BlogSerializer  # noqa
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)


class BlogViewSet(ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, GenericViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

```

# 📈 REST API

### Standalone mode

If you are planning to use `drf_localize`'s REST API endpoints add package urls in your project.

```python
from django.urls import (include, path, )

urlpatterns = [
    ...,
    path('drf_localize', include('drf_localize.urls', namespace='localize')),
    ...,
]
```

### Create localize key

```http
POST /drf_localize/localize/keys
```

| Parameter | Type     | Description            |
|:----------|:---------|:-----------------------|
| `code`    | `string` | **Required**. *Unique* |
| `i18n`    | `object` | **Optional**.          |

```json
{
  "code": "DRF Localize",
  "i18n": {
    "en": "DRF Localize",
    "ro": "DRF Localizare",
    "ru": "DRF Локализация"
  }
}
```

#### Update localize key

```http
PATCH /drf_localize/localize/keys/:id
```

| Parameter | Type     | Description         |
|:----------|:---------|:--------------------|
| `:id`     | `string` | **Required**. |
| `code`    | `string` | **Required**. *Unique* |
| `i18n`    | `object` | **Optional**.       |

```json
{
  "i18n": {
    "en": "DRF Localizes",
    "ro": "DRF Localizare",
    "ru": "DRF Локализация"
  }
}
```

### Create localize namespace key

```http
POST /drf_localize/localize/keys
```

| Parameter | Type     | Description            |
|:----------|:---------|:-----------------------|
| `code`    | `string` | **Required**. *Unique* |
| `i18n`    | `object` | **Optional**.          |
| `type`    | `string` | **Required**.          |

```json
{
  "code": "global",
  "i18n": {
    "en": {
      "localize": "DRF Localizes"
    },
    "ro": {
      "localize": "DRF Localizare"
    },
    "ru": {
      "localize": "DRF Локализация"
    }
  },
  "type": "NAMESPACE"
}
```

#### Update localize namespace key

```http
PATCH /drf_localize/localize/keys/:id
```

| Parameter | Type     | Description         |
|:----------|:---------|:--------------------|
| `:id`     | `string` | **Required**. |
| `code`    | `string` | **Required**. *Unique* |
| `i18n`    | `object` | **Optional**.       |
| `type`    | `string` | **Required**.          |

```json
{
  "i18n": {
    "en": {
      "localize": "DRF Localize"
    },
    "ro": {
      "localize": "DRF Localizare"
    },
    "ru": {
      "localize": "DRF Локализация"
    }
  },
  "type": "NAMESPACE"
}
```

#### Retrieve localize namespace keys

```http
GET /drf_localize/localize/keys?search=NAMESPACE
```

#### Download platform specific localize key file

```http
GET /drf_localize/localize/keys/:platform/:language/file
```

| Parameter   | Type     | Description                                 |
|:------------|:---------|:--------------------------------------------|
| `:platform` | `string` | **Required**. `ios`/ `android` / `web`      |
| `:language` | `string` | **Required**. `en`/ any other language code |

#### Download platform specific localize keys zip file

```http
GET /drf_localize/localize/keys/:platform/zip
```

| Parameter   | Type     | Description                                 |
|:------------|:---------|:--------------------------------------------|
| `:platform` | `string` | **Required**. `ios`/ `android` / `web`      |

#### Download all platform specific localize keys in a single zip file

```http
GET /drf_localize/localize/keys/zip
```

### Service mode

You will need to add a middleware class:

```python
# This middleware listens to `X-API-Key` key header value and finds your application.

MIDDLEWARE = [
    ...,
    'drf_localize.middlewares.LocalizeApplicationMiddleware',
    ...,
]
```

then add `X-API-Key` header in standalone mode endpoints:

| Header         | Type    | Description                        |
|:---------------|:--------|:-----------------------------------|
| `X-API-Key`| `string`| **Required**. Your application key |

### Create application

```http
POST /drf_localize/localize/applications
```

| Parameter | Type     | Description         |
|:----------|:---------|:--------------------|
| `title`   | `string` | **Optional**.|
| `description`    | `string` | **Optional**.       |

#### Retrieve application

```http
GET /drf_localize/localize/application
```

| Header         | Type    | Description                        |
|:---------------|:--------|:-----------------------------------|
| `X-API-Key`| `string`| **Required**. Your application key |

#### Attach application languages

```http
POST /drf_localize/localize/application/languages
```

| Parameter | Type     | Description   |
|:----------|:---------|:--------------|
| `languages_id`   | `array`  | **Required**. |

| Header         | Type    | Description                        |
|:---------------|:--------|:-----------------------------------|
| `X-API-Key`| `string`| **Required**. Your application key |

```json
{
  "languages_id": [
    2,
    1
  ]
}
```

#### Detach application languages

```http
DELETE /drf_localize/localize/application/languages
```

| Parameter | Type     | Description   |
|:----------|:---------|:--------------|
| `languages_id`   | `array`  | **Required**. |

| Header         | Type    | Description                        |
|:---------------|:--------|:-----------------------------------|
| `X-API-Key`| `string`| **Required**. Your application key |

```json
{
  "languages_id": [
    1
  ]
}
```

#### Retrieve application languages

```http
GET /drf_localize/localize/application/languages
```

| Header         | Type    | Description                        |
|:---------------|:--------|:-----------------------------------|
| `X-API-Key`| `string`| **Required**. Your application key |

```json
[
  {
    "code": "ab",
    "name": "Abkhaz",
    "native": "аҧсуа"
  }
]
```

# 📦️ Library

```python
from drf_localize import localize

# Set translatable key translation.
localize.set_key('Welcome').set_en('Welcome').set_ro('Bine ati venit').set_pt('Receber')  # noqa

# Set translatable namespace translation.
localize.set_key_namespace('common').set_en({
    'welcome': 'Welcome', 'order': 'Order'
}).set_ro({
    'welcome': 'Bine ati venit', 'order': 'Ordin'
}).set_pt({
    'welcome': 'Receber', 'order': 'Pedido'
})

# Build 'en' translation file for iOS
localize.build(language='en')
file = localize.to_platform(platform='IOS')  # noqa

# Build translations zip file for iOS
file = localize.build_zip(platform='IOS')  # noqa

# Build translations zip file for ANDROID
file = localize.build_zip(platform='ANDROID')  # noqa

# Build translations zip file for WEB
file = localize.build_zip(platform='WEB')  # noqa

# Build translations zip file for every platform
file = localize.build_zip()  # noqa
```

## 📌 Library helpers

```python

# from drf_localize import localize_key_type

class LocalizeKeyType:
    KEY_NAMESPACE = 'NAMESPACE'
    KEY_PLAIN = 'PLAIN'

    KEY_TYPES = [KEY_NAMESPACE, KEY_PLAIN]
    KEY_CHOICES = (
        (KEY_NAMESPACE, KEY_NAMESPACE),
        (KEY_PLAIN, KEY_PLAIN)
    )


# from drf_localize import localize_platform

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
```

# ⚗️ Internal Serializer Classes

Uses `I18N` serializer to transform localize field

> **Inherit this `I18NModelSerializer` serializer in your model serializer**

```python
from rest_framework.serializers import ModelSerializer


class I18NModelSerializer(ModelSerializer):  # noqa
    ...
```

Transforms localize field into i18n json field with translations

```python
from rest_framework.serializers import Serializer


class I18N(Serializer):  # noqa
    ...
```

# 👥 Contributing

Pull requests are always appreciated. Open issues addressing pull requests.

Flow:

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Test your changes to the best of your ability.
4. Update the documentation to reflect your changes if they add or changes current functionality.
5. Commit your changes (`git commit -am 'Added some feature'`).
6. Push to the branch (`git push origin my-new-feature`)
7. Create new Pull Request