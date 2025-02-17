from rest_framework import serializers
from rest_framework.generics import ListAPIView

from helsinki_notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "modified_at",
            "type_name",
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

    def get_type_name(self, obj):
        return obj.type_name


class NotificationList(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.valid_objects.all()
