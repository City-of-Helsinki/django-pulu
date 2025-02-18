from contextlib import contextmanager
from unittest import mock

import pytest

import helsinki_notification.settings as app_settings


@pytest.fixture
def override_settings():
    """NOTE: Do not set any URL-related setting with this in conjunction with anything
    that resolves URLs (e.g. client requests, django.urls.reverse); resolved URLs are
    cached and this will cause issues."""
    from importlib import reload

    import helsinki_notification.settings

    @contextmanager
    def _override(**options):
        # Patch settings in django.conf rather than in helsinki_notification.settings;
        # the latter gets reloaded later on which makes the module import the mocked
        # version of django.conf.settings.
        patcher = mock.patch("django.conf.settings")
        mock_settings = patcher.start()
        for k, v in options.items():
            setattr(mock_settings, k, v)
        reload(helsinki_notification.settings)

        try:
            yield
        finally:
            patcher.stop()
            reload(helsinki_notification.settings)

    return _override


def test_list_url(override_settings):
    with override_settings(HELSINKI_NOTIFICATION_LIST_URL="custom_list"):
        assert app_settings.LIST_URL == "custom_list"
