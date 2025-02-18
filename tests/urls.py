from django.contrib import admin
from django.urls import include, path

import helsinki_notification.contrib.rest_framework.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "drf/",
        include(
            helsinki_notification.contrib.rest_framework.urls,
            namespace="rest_framework",
        ),
    ),
]
