import pytest
from unittest import mock
from PigeonBox.status import *
from car import Car


def test_car_init():
    car = Car(vin="1234", price=10000)
    assert car.vin == "1234"
    assert car.price == 10000
    assert car.status == status.Status.AVAILABLE


def test_car_update_mileage():
    car = Car()
    car.UpdateMileage(50000)
    assert car.info["mileage"] == 50000


def test_car_update_warranty():
    car = Car()
    car.UpdateWarranty("extended")
    assert "extended" in car.protection["warranty"]


def test_car_to_dict():
    car = Car(vin="1234", price=10000)
    car_dict = car.to_dict()
    assert car_dict["vin"] == "1234"
    assert car_dict["price"] == 10000
    assert car_dict["status"] == "available"


def test_car_serialize():
    car = Car(vin="1234", price=10000)
    serialized_car = Car.serialize(car)
    assert serialized_car["vin"] == "1234"
    assert serialized_car["price"] == 10000
    assert serialized_car["status"] == "available"


def test_car_is_available():
    car = Car()
    assert car.isAvailable() == True
    car.SetStatus("sold")
    assert car.isAvailable() == False


def test_car_update_price():
    car = Car()
    car.UpdatePrice(15000)
    assert car.price == 15000


def test_car_get_details():
    car = Car(vin="1234", info={"year": 2020, "make": "Honda", "model": "Civic"}, package="basic", performance={"engine": "1.5L", "transmission": "automatic"}, design={"interior": "cloth", "exterior": "red"}, handling=["power steering", "front-wheel drive"], comfort=["AC", "cruise control"], entertainment=["FM radio", "Bluetooth"], protection={"maintenance": "oil changes", "warranty": ["basic", "extended"]}, price=20000, status=status.Status.AVAILABLE)
    expected_result = "\n\u001b[1m2020 Civic Honda\u001b[0m \u001b[92m$20,000.00\u001b[0m \u001b[4mavailable\u001b[0m\n1234 with basic package\nPerformance\nEngine: 1.5L, Transmission: automatic\nMileage: 0 miles\n\u001b[1mDesign\u001b[0m\nInterior design: cloth\nExterior design: red\n\u001b[1mExtras\u001b[0m\nComfort: ['AC', 'cruise control']\nEntertainment ['FM radio', 'Bluetooth']\n\u001b[1mProtection plans\u001b[0m\nMaintenance oil changes\nWarranty plans ['basic', 'extended']"
    assert car.getDetails() == expected_result


def test_car_eq():
    car1 = Car(vin="1234")
    car2 = Car(vin="5678")
    car3 = Car(vin="1234")
    assert car1 == car3
    assert car1 != car2
