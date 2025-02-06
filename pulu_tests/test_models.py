from collections.abc import Collection
from datetime import datetime, timedelta
from typing import Union

import pytest
from django.db.models import QuerySet
from django.utils import timezone
from freezegun import freeze_time

from pulu.models import Notification


def _values_list(objects: Union[Collection, QuerySet[Notification]], *fields: str):
    flat = len(fields) == 1
    if isinstance(objects, QuerySet):
        return objects.values_list(*fields, flat=flat)
    if flat:
        return [getattr(obj, fields[0]) for obj in objects]
    return [(getattr(obj, field) for field in fields) for obj in objects]


def assert_qs_values(
    qs: QuerySet, values: Collection, *fields: str, ordered: bool = False
):
    """Assert that the values of the given fields match between a query set and
    a collection of objects."""
    assert len(qs) == len(values)
    if ordered:
        assert list(_values_list(qs, *fields)) == _values_list(values, *fields)
    else:
        assert set(_values_list(qs, *fields)) == set(_values_list(values, *fields))


@freeze_time("2025-01-01T12:00:00Z")
@pytest.mark.django_db
def test_notification_model_managers(notification_factory):
    expired_notification = notification_factory(
        validity_period_start=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
        validity_period_end=datetime.fromisoformat("2025-01-01T11:59:59+00:00"),
    )
    future_notification = notification_factory(
        validity_period_start=datetime.fromisoformat("2025-01-01T12:00:01+00:00"),
        validity_period_end=datetime.fromisoformat("2025-01-02T00:00:00+00:00"),
    )
    valid_notifications = [
        # Middle of validity period
        notification_factory(
            validity_period_start=datetime.fromisoformat("2025-01-01T11:00:00+00:00"),
            validity_period_end=datetime.fromisoformat("2025-01-01T13:00:00+00:00"),
        ),
        # First valid second
        notification_factory(
            validity_period_start=datetime.fromisoformat("2025-01-01T12:00:00+00:00"),
            validity_period_end=datetime.fromisoformat("2025-01-01T13:00:00+00:00"),
        ),
        # Last valid second
        notification_factory(
            validity_period_start=datetime.fromisoformat("2025-01-01T11:00:00+00:00"),
            validity_period_end=datetime.fromisoformat("2025-01-01T12:00:00+00:00"),
        ),
        # Valid only at 12:00:00
        notification_factory(
            validity_period_start=datetime.fromisoformat("2025-01-01T12:00:00+00:00"),
            validity_period_end=datetime.fromisoformat("2025-01-01T12:00:00+00:00"),
        ),
    ]
    created_notifications = [
        expired_notification,
        future_notification,
    ] + valid_notifications

    assert_qs_values(Notification.objects.all(), created_notifications, "id")
    assert_qs_values(Notification.valid_objects.all(), valid_notifications, "id")


@freeze_time("2025-01-01T12:00:00Z")
@pytest.mark.django_db
def test_notification_default_ordering(valid_notification_factory):
    """Notifications should order with the following priority:
    1. Type, error > warning > info (desc)
    2. Validity period start, most recent first (desc)
    3. Creation time, newest first (desc)
    """
    last_hour = timezone.now() - timedelta(hours=1)
    last_day = timezone.now() - timedelta(days=1)
    last_month = timezone.now() - timedelta(days=30)
    expected_order = [
        # Error
        valid_notification_factory(
            type=Notification.Type.ERROR, validity_period_start=last_hour
        ),
        valid_notification_factory(
            type=Notification.Type.ERROR, validity_period_start=last_hour
        ),
        valid_notification_factory(
            type=Notification.Type.ERROR, validity_period_start=last_day
        ),
        valid_notification_factory(
            type=Notification.Type.ERROR, validity_period_start=last_day
        ),
        valid_notification_factory(
            type=Notification.Type.ERROR, validity_period_start=last_month
        ),
        valid_notification_factory(
            type=Notification.Type.ERROR, validity_period_start=last_month
        ),
        # Alert
        valid_notification_factory(
            type=Notification.Type.ALERT, validity_period_start=last_hour
        ),
        valid_notification_factory(
            type=Notification.Type.ALERT, validity_period_start=last_day
        ),
        valid_notification_factory(
            type=Notification.Type.ALERT, validity_period_start=last_day
        ),
        valid_notification_factory(
            type=Notification.Type.ALERT, validity_period_start=last_day
        ),
        valid_notification_factory(
            type=Notification.Type.ALERT, validity_period_start=last_month
        ),
        # Info
        valid_notification_factory(
            type=Notification.Type.INFO, validity_period_start=last_hour
        ),
        valid_notification_factory(
            type=Notification.Type.INFO, validity_period_start=last_day
        ),
        valid_notification_factory(
            type=Notification.Type.INFO, validity_period_start=last_day
        ),
        valid_notification_factory(
            type=Notification.Type.INFO, validity_period_start=last_day
        ),
    ]

    assert_qs_values(
        Notification.valid_objects.all(), expected_order, "id", ordered=True
    )
