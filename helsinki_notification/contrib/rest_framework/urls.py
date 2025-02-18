from django.urls import re_path

from helsinki_notification import settings
from helsinki_notification.contrib.rest_framework import views

app_name = "helsinki_notification"

urlpatterns = [
    re_path(
        settings.LIST_URL, views.NotificationList.as_view(), name="notification-list"
    )
]
