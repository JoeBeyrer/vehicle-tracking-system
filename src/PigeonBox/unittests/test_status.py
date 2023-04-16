import pytest
from unittest import mock
from PigeonBox.status import *

@pytest.mark.parametrize(
    "status_string, expected_status",
    [
        ("available", Status.AVAILABLE),
        ("ordered", Status.ORDERED),
        ("backorder", Status.BACKORDER),
        ("delivered", Status.DELIVERED),
        ("invalid", None),
    ]
)
def test_strToStatus(status_string, expected_status):
    assert strToStatus(status_string) == expected_status

@pytest.mark.parametrize(
    "status, expected_string",
    [
        (Status.AVAILABLE, "available"),
        (Status.ORDERED, "ordered"),
        (Status.BACKORDER, "backorder"),
        (Status.DELIVERED, "delivered"),
    ]
)
def test_StatusToStr(status, expected_string):
    assert StatusToStr(status) == expected_string
