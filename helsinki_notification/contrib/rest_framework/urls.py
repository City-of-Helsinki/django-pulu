from django.urls import re_path

from helsinki_notification.contrib.rest_framework import views

urlpatterns = [
    re_path(
        "^notifications/$", views.NotificationList.as_view(), name="notification-list"
    )
]
