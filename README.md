# 🔔 django-helsinki-notification

Notifications for City of Helsinki Django apps 🔔


# 🚀 Overview

Django Helsinki Notification is a notification manager for City of Helsinki Django
apps.

* Manage notifications through Django Admin
* Support for Finnish, Swedish and English translations
* "Batteries included" list endpoint for [Django REST Framework][drf-url]


# 📋 Requirements

- Python 3.9+
- Django 4.2, 5.0, 5.1


# 🛠️ Installation

Install using pip:
```shell
pip install django-helsinki-notification@git+https://github.com/City-of-Helsinki/django-helsinki-notification
```

if your project does not already have [Django REST Framework (DRF)][drf-url] installed, and you
want to use the included DRF module, install the `rest_framework` extra:
```shell
pip install django-helsinki-notification[rest_framework]@git+https://github.com/City-of-Helsinki/django-helsinki-notification
```

Add `"helsinki_notification"` to your `INSTALLED_APPS` setting:
```python
INSTALLED_APPS = [
    ...,
    "helsinki_notification",
]
```

## Setting up the API

To access the notifications through an API, you need to set up a list endpoint. There
are two ways to do this:

1. Use the included Django REST Framework module
2. Implement your own view


### Django REST Framework integration

Include `helsinki_notification.contrib.rest_framework.urls` to your URLconf, e.g:

```python
from django.urls import path, include

import helsinki_notification.contrib.rest_framework.urls

urlpatterns = [
    ...,
    path("", include(helsinki_notification.contrib.rest_framework.urls))
]
```

### Implementing your own view

For other use cases, you can implement your own views using the
`helsinki_notification.models.Notification` model. For example, here's a simplified
Django implementation of a list endpoint:

```python
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from helsinki_notification.models import Notification

@require_GET
def my_custom_notification_list(request):
    fields = ("id", "title_fi", "title_sv", "title_en")
    queryset = Notification.valid_objects.all()
    return JsonResponse(
        {
            "results": [
                {field: getattr(obj, field) for field in fields} for obj in queryset
            ]
        }
    )
```

---

# 🤖 For developers

## 📋 Prerequisites

- [Hatch][hatch-url]


## 🏗️ Setup

1. Create the default environment:
    ```shell
    hatch env create
    ```

2. Set up Django with optional dummy data:
    ```shell
    hatch run manage migrate
    hatch run manage loaddata quickstart
    ```

3. Run the development server:
    ```shell
    hatch run manage runserver
    ```

Access the admin page with username `admin` and password `admin` in
http://localhost:8000/admin.

## 🧪 Testing

Run the tests with:
```shell
hatch test
```

Test all environments in the matrix with:
```shell
hatch test -a
```


[hatch-url]: https://hatch.pypa.io/latest/install/
[drf-url]: https://www.django-rest-framework.org/
