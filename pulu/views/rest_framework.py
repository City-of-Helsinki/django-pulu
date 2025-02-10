from rest_framework import serializers
from rest_framework.generics import ListAPIView

from pulu.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "modified_at",
            "type",
            "title_fi",
            "title_sv",
            "title_en",
            "content_fi",
            "content_sv",
            "content_en",
            "external_url_fi",
            "external_url_sv",
            "external_url_en",
            "external_url_title_fi",
            "external_url_title_sv",
            "external_url_title_en",
        ]


class NotificationList(ListAPIView):
    queryset = Notification.valid_objects.all()
    serializer_class = NotificationSerializer
