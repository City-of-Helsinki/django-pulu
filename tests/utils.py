from typing import Collection, Union

from django.db.models import QuerySet

from helsinki_notification.models import Notification


def values_list(objects: Union[Collection, QuerySet[Notification]], *fields: str):
    flat = len(fields) == 1
    if isinstance(objects, QuerySet):
        return objects.values_list(*fields, flat=flat)
    if flat:
        return [getattr(obj, fields[0]) for obj in objects]
    return [(getattr(obj, field) for field in fields) for obj in objects]


def values_list_from_dict(objects: Collection[dict], *fields: str):
    flat = len(fields) == 1
    if flat:
        return [obj.get(fields[0]) for obj in objects]
    return [(obj.get(field) for field in fields) for obj in objects]


def assert_qs_values(
    qs: QuerySet, values: Collection, *fields: str, ordered: bool = False
):
    """Assert that the values of the given fields match between a query set and
    a collection of objects."""
    assert len(qs) == len(values)
    if ordered:
        assert list(values_list(qs, *fields)) == values_list(values, *fields)
    else:
        assert set(values_list(qs, *fields)) == set(values_list(values, *fields))
