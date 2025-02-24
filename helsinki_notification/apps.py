from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HelsinkiNotificationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "helsinki_notification"
    verbose_name = _("Notifications")
