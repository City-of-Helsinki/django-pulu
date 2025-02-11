from datetime import datetime

import pytest
from freezegun import freeze_time

from helsinki_notification.models import Notification
from tests.utils import assert_qs_values


@freeze_time("2025-01-01T12:00:00Z")
@pytest.mark.django_db
def test_notification_model_managers(notification_factory, make_relative_time):
    relative_time = make_relative_time(
        datetime.fromisoformat("2025-01-01T12:00:00+00:00")
    )
    expired_notification = notification_factory(
        validity_period_start=relative_time.last_hour,
        validity_period_end=relative_time.last_second,
    )
    future_notification = notification_factory(
        validity_period_start=relative_time.next_second,
        validity_period_end=relative_time.tomorrow,
    )
    valid_notifications = [
        # Middle of validity period
        notification_factory(
            validity_period_start=relative_time.last_hour,
            validity_period_end=relative_time.next_hour,
        ),
        # First valid second
        notification_factory(
            validity_period_start=relative_time.now,
            validity_period_end=relative_time.next_hour,
        ),
        # Last valid second
        notification_factory(
            validity_period_start=relative_time.last_hour,
            validity_period_end=relative_time.now,
        ),
        # Valid only at 12:00:00
        notification_factory(
            validity_period_start=relative_time.now,
            validity_period_end=relative_time.now,
        ),
    ]
    created_notifications = [
        expired_notification,
        future_notification,
    ] + valid_notifications

    assert_qs_values(Notification.objects.all(), created_notifications, "id")
    assert_qs_values(Notification.valid_objects.all(), valid_notifications, "id")


@pytest.mark.django_db
def test_notification_default_ordering(valid_notification_factory, make_relative_time):
    """Notifications should order with the following priority:
    1. Type, error > warning > info (desc)
    2. Validity period start, most recent first (desc)
    3. Creation time, newest first (desc)
    """
    relative_time = make_relative_time(
        datetime.fromisoformat("2025-01-01T12:00:00+00:00")
    )

    def make_error(*args, **kwargs):
        return valid_notification_factory(*args, **kwargs, type=Notification.Type.ERROR)

    def make_alert(*args, **kwargs):
        return valid_notification_factory(*args, **kwargs, type=Notification.Type.ALERT)

    def make_info(*args, **kwargs):
        return valid_notification_factory(*args, **kwargs, type=Notification.Type.INFO)

    notifications = [
        # Error
        make_error(validity_period_start=relative_time.last_second),  # 0
        make_error(validity_period_start=relative_time.last_second),  # 1
        make_error(validity_period_start=relative_time.last_hour),  # 2
        make_error(validity_period_start=relative_time.last_hour),  # 3
        make_error(validity_period_start=relative_time.yesterday),  # 4
        make_error(validity_period_start=relative_time.yesterday),  # 5
        # Alert
        make_alert(validity_period_start=relative_time.last_second),  # 6
        make_alert(validity_period_start=relative_time.last_hour),  # 7
        make_alert(validity_period_start=relative_time.last_hour),  # 8
        make_alert(validity_period_start=relative_time.last_hour),  # 9
        make_alert(validity_period_start=relative_time.yesterday),  # 10
        # Info
        make_info(validity_period_start=relative_time.last_second),  # 11
        make_info(validity_period_start=relative_time.last_hour),  # 12
        make_info(validity_period_start=relative_time.last_hour),  # 13
        make_info(validity_period_start=relative_time.last_hour),  # 14
    ]
    expected_order = [
        notifications[i] for i in [1, 0, 3, 2, 5, 4, 6, 9, 8, 7, 10, 11, 14, 13, 12]
    ]

    with freeze_time("2025-01-01T12:00:00Z"):
        assert_qs_values(
            Notification.valid_objects.all(), expected_order, "id", ordered=True
        )
