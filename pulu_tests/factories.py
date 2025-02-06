from datetime import timedelta

import factory
from django.utils import timezone
from pytest_factoryboy import register

from pulu.models import Notification


@register
class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification


@register
class ValidNotificationFactory(NotificationFactory):
    validity_period_start = factory.LazyAttribute(lambda _: timezone.now())
    validity_period_end = factory.LazyAttribute(
        lambda o: o.validity_period_start + timedelta(days=999)
    )
