from django.contrib import admin
from django.urls import path

import helsinki_notification.views.rest_framework

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "drf/notifications",
        helsinki_notification.views.rest_framework.NotificationList.as_view(),
    ),
]
