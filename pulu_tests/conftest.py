from pytest_factoryboy import register

from pulu_tests.factories import NotificationFactory, ValidNotificationFactory

register(NotificationFactory)
register(ValidNotificationFactory)
