from django.contrib import admin
from django.utils.translation import gettext as _

from pulu.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["__str__", "type", "validity_period_start", "validity_period_end"]
    readonly_fields = ["created_at", "modified_at"]
    fieldsets = [
        (
            _("Notification details"),
            {
                "fields": [
                    "title_fi",
                    "content_fi",
                    "title_sv",
                    "content_sv",
                    "title_en",
                    "content_en",
                    "type",
                ]
            },
        ),
        (
            _("External URL"),
            {
                "fields": [
                    "external_url_title_fi",
                    "external_url_fi",
                    "external_url_title_sv",
                    "external_url_sv",
                    "external_url_title_en",
                    "external_url_en",
                ]
            },
        ),
        (
            _("Validity period"),
            {"fields": ["validity_period_start", "validity_period_end"]},
        ),
        (
            _("System fields"),
            {
                "fields": [
                    "created_at",
                    "modified_at",
                ]
            },
        ),
    ]
