import factory
from pytest_factoryboy import register

from pulu.models import Notification


@register
class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification
