# Changelog

## 0.1.0 (2025-02-26)


### ⚠ BREAKING CHANGES

* make url titles non-nullable
* replace views.rest_framework with contrib.rest_framework module
* **views:** replace type field with type_name
* recreate initial migration
* rename project to django-helsinki-notification
* add default ordering for notification
* change type field's type to int

### Features

* Add default ordering for notification ([f1d6999](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/f1d69995b99e02ed13a4e7bd0e20b8cc3f5d9ce7))
* Add human-readable name for the app ([455c5a5](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/455c5a5879286397f8629f64aad7340991a9500b))
* Add notification admin view ([b97acdf](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/b97acdfc58e63ea3f93fd70bedac716416ce35d9))
* Add notification model and test project ([195e799](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/195e799f7c581e6b08e93e4b540baa6ea5d2b3a6))
* Add type_name in Notification ([7ccb659](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/7ccb6596fcfa37a27e67f9ef891f5235bdb6db26))
* Add valid_objects manager for notifications ([30a913f](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/30a913fe7290a5cd1fc383f67b189967ff6257d2))
* Add view for rest framework ([2c39b97](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/2c39b9782e72c7e94cc6afd355a697510c11d7b9))
* Change type field's type to int ([d57d358](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/d57d3586b894306eb1409a8f072b54b022399d01))
* Make the notification list url configurable ([8f436bd](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/8f436bd9a06dec1896f20397aca5f4593f619227))
* Replace views.rest_framework with contrib.rest_framework module ([a64a03a](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/a64a03a781c131f6d6e9c96b56d112fd81b73260))
* **views:** Replace type field with type_name ([8c3911b](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/8c3911b43ee24755a8946680a1820fad0e975cf1))


### Bug Fixes

* Add validation for validity period ([a7c12fe](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/a7c12fec64829fd9103a5803ea2f22735c2461ee))
* Filter zero duration notifications in valid_objects ([a443487](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/a443487452b22a3ce530ed5087402da06969a7db))
* Make url titles non-nullable ([8da81c2](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/8da81c2c744af8ec1947de1199a4433ecaa80641))
* **views:** Replace queryset with get_queryset ([89483c3](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/89483c324bf6869edd3aaeded31b017c410b9f6e))


### Documentation

* Write readme ([8b73069](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/8b73069c2c7c99a21f5b50dc8397e6d69fe0e9bc))


### Miscellaneous Chores

* Recreate initial migration ([eff954b](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/eff954b7d5075c0b38fe276ba98fc6d7f44def51))
* Rename project to django-helsinki-notification ([c3df2c4](https://github.com/City-of-Helsinki/django-helsinki-notification/commit/c3df2c415d8e07c5f0eb994ce8137637663c7465))
