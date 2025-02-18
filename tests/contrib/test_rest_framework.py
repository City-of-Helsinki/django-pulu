import pytest
from freezegun import freeze_time

from helsinki_notification.contrib.rest_framework.views import NotificationSerializer
from helsinki_notification.models import Notification
from tests.utils import values_list, values_list_from_dict


@freeze_time("2025-01-01T12:00:00Z")
@pytest.mark.django_db
def test_list_endpoint(
    notification_factory, valid_notification_factory, relative_now, client
):
    notification_factory(
        title_en="Past notification",
        validity_period_start=relative_now.yesterday,
        validity_period_end=relative_now.last_second,
    )
    notification_factory(
        title_en="Future notification",
        validity_period_start=relative_now.next_hour,
        validity_period_end=relative_now.far_future,
    )
    expected_order = [
        valid_notification_factory(type=Notification.Type.ERROR),
        valid_notification_factory(type=Notification.Type.ALERT),
        valid_notification_factory(type=Notification.Type.INFO),
    ]

    response = client.get("/drf/notifications/")

    assert response.status_code == 200
    assert len(response.data) == len(expected_order)
    assert values_list_from_dict(response.data, "id") == values_list(
        expected_order, "id"
    )


def test_type_name_field(valid_notification_factory):
    notification = valid_notification_factory.build(type=Notification.Type.INFO)
    serializer = NotificationSerializer(instance=notification)
    assert serializer.data["type_name"] == "INFO"
