from django.conf import settings as django_settings

# URL for the list endpoint.
LIST_URL = getattr(
    django_settings, "HELSINKI_NOTIFICATION_LIST_URL", r"^notifications/$"
)
