from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class ValidNotificationManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super()
            .get_queryset()
            .filter(validity_period_start__lte=now, validity_period_end__gt=now)
        )


class Notification(models.Model):
    class Type(models.IntegerChoices):
        INFO = 20, _("Information")
        ALERT = 30, _("Alert")
        ERROR = 40, _("Error")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation time")
    )
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Modification time")
    )
    validity_period_start = models.DateTimeField(verbose_name=_("Valid from"))
    validity_period_end = models.DateTimeField(verbose_name=_("Valid until"))
    type = models.IntegerField(
        choices=Type.choices,
        default=Type.INFO,
        verbose_name=_("Notification type"),
    )

    # Title
    title_fi = models.CharField(max_length=200, verbose_name=_("Title (Finnish)"))
    title_sv = models.CharField(max_length=200, verbose_name=_("Title (Swedish)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Title (English)"))

    # Content
    content_fi = models.TextField(verbose_name=_("Content (Finnish)"))
    content_sv = models.TextField(verbose_name=_("Content (Swedish)"))
    content_en = models.TextField(verbose_name=_("Content (English)"))

    # External URL
    external_url_fi = models.URLField(
        blank=True, verbose_name=_("External URL (Finnish)")
    )
    external_url_sv = models.URLField(
        blank=True, verbose_name=_("External URL (Swedish)")
    )
    external_url_en = models.URLField(
        blank=True, verbose_name=_("External URL (English)")
    )

    # External URL title
    external_url_title_fi = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name=_("External URL title (Finnish)"),
    )
    external_url_title_sv = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name=_("External URL title (Swedish)"),
    )
    external_url_title_en = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name=_("External URL title (English)"),
    )

    objects = models.Manager()
    valid_objects = ValidNotificationManager()

    class Meta:
        ordering = ["-type", "-validity_period_start", "-created_at"]
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    @cached_property
    def _localized_title(self):
        lang = get_language()
        if lang.startswith("fi"):
            return self.title_fi
        if lang.startswith("sv"):
            return self.title_sv
        return self.title_en

    def __str__(self):
        return self._localized_title

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.validity_period_start >= self.validity_period_end:
            raise ValidationError(
                "The validity period's start must occur before its end."
            )

    @property
    def type_name(self) -> str:
        return Notification.Type(self.type).name
