from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
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
        title_en="Past notification, should NOT show up",
        validity_period_start=relative_time.last_hour,
        validity_period_end=relative_time.last_second,
    )
    future_notification = notification_factory(
        title_en="Future notification, should NOT show up",
        validity_period_start=relative_time.next_second,
        validity_period_end=relative_time.tomorrow,
    )
    valid_notifications = [
        notification_factory(
            title_en="Middle of validity period",
            validity_period_start=relative_time.last_hour,
            validity_period_end=relative_time.next_hour,
        ),
        notification_factory(
            title_en="First valid second",
            validity_period_start=relative_time.now,
            validity_period_end=relative_time.next_hour,
        ),
        notification_factory(
            title_en="Last valid second",
            validity_period_start=relative_time.last_hour,
            validity_period_end=relative_time.next_second,
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


@pytest.mark.parametrize(
    "type_value, expected",
    [
        (Notification.Type.INFO, "INFO"),
        (Notification.Type.ALERT, "ALERT"),
        (Notification.Type.ERROR, "ERROR"),
    ],
)
@pytest.mark.django_db
def test_notification_type_name(valid_notification_factory, type_value, expected):
    notification = valid_notification_factory(type=type_value)
    assert notification.type_name == expected


@pytest.mark.django_db
def test_notification_cannot_start_after_its_end(notification_factory, relative_now):
    with pytest.raises(ValidationError):
        notification_factory(
            validity_period_start=relative_now.far_future,
            validity_period_end=relative_now.last_day,
        )


@pytest.mark.django_db
def test_notification_cannot_have_zero_duration(notification_factory, relative_now):
    with pytest.raises(ValidationError):
        notification_factory(
            validity_period_start=relative_now.now,
            validity_period_end=relative_now.now,
        )
