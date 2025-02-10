from django.contrib import admin
from django.urls import path

import pulu.views.rest_framework

urlpatterns = [
    path("admin/", admin.site.urls),
    path("drf/notifications", pulu.views.rest_framework.NotificationList.as_view()),
]
