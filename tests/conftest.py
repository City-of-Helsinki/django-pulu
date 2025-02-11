from datetime import datetime, timedelta
from functools import cached_property

import pytest
from django.utils import timezone
from pytest_factoryboy import register

from tests.factories import NotificationFactory, ValidNotificationFactory

register(NotificationFactory)
register(ValidNotificationFactory)


class RelativeTime:
    def __init__(self, reference_point: datetime = None):
        self._now = reference_point

    @cached_property
    def now(self):
        if self._now:
            return self._now
        return timezone.now()

    @property
    def last_second(self):
        return self.now - timedelta(seconds=1)

    @property
    def last_hour(self):
        return self.now - timedelta(hours=1)

    @property
    def yesterday(self):
        return self.now - timedelta(days=1)

    last_day = yesterday

    @property
    def next_second(self):
        return self.now + timedelta(seconds=1)

    @property
    def next_hour(self):
        return self.now + timedelta(hours=1)

    @property
    def tomorrow(self):
        return self.now + timedelta(days=1)

    @property
    def far_future(self):
        return self.now + timedelta(days=999)


@pytest.fixture
def relative_now():
    return RelativeTime()


@pytest.fixture
def make_relative_time():
    def _make_relative_time(*args, **kwargs):
        return RelativeTime(*args, **kwargs)

    return _make_relative_time
