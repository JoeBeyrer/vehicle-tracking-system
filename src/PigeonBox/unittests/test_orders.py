from PigeonBox.orders import *
import pytest
from unittest import mock
from datetime import datetime

# super straight forward file to test the class and its methods. May require some minor changes
@pytest.fixture
def sample_order():
    sample_car = mock.MagicMock()
    sample_buyer = mock.MagicMock()
    sample_employee = mock.MagicMock()
    return Order(1, car=sample_car, buyer=sample_buyer, dateBought='2022-04-15', employee=sample_employee)


def test_getUser(sample_order):
    assert sample_order.getUser() == sample_order.buyer


def test_getCar(sample_order):
    assert sample_order.getCar() == sample_order.car


def test_getSeller(sample_order):
    assert sample_order.getSeller() == sample_order.salesBy


def test_getDate(sample_order):
    assert sample_order.getDate() == datetime(2022, 4, 15)


def test_getId(sample_order):
    assert sample_order.getId() == 1


def test_getDateJoined(sample_order):
    assert sample_order.getDateJoined() == '2022-04-15'


def test_to_dict(sample_order):
    expected_output = {
        "id": 1,
        "carVin": sample_order.car.getVin(),
        "buyer": sample_order.buyer.getEmail(),
        "soldBy": sample_order.salesBy.getUsername(),
        "dateBought": '2022-04-15'
    }
    assert sample_order.to_dict() == expected_output


def test_serialize(sample_order):
    expected_output = {
        "id": 1,
        "carVin": sample_order.car.getVin(),
        "buyer": sample_order.buyer.getEmail(),
        "soldBy": sample_order.salesBy.getUsername(),
        "dateBought": '2022-04-15'
    }
    assert Order.serialize(sample_order) == expected_output


def test_RemoveOrder(sample_order):
    sample_order.buyer.orders = [sample_order]
    sample_order.RemoveOrder()
    assert sample_order.buyer.orders == []
    assert sample_order.car.SetStatus.call_args == mock.call('available')


def test_orderDetails(sample_order):
    sample_car = sample_order.car
    sample_buyer = sample_order.buyer
    sample_sales_by = sample_order.salesBy
    expected_output = f"\nCar:\n{sample_car.getDetails()}\n\nSales by: {sample_sales_by}\n\nCustomer {sample_buyer.getDetails()}\n"
    assert sample_order.orderDetails() == expected_output


def test_str(sample_order):
    sample_car_make = sample_order.car.getCarInfo()['make']
    sample_car_model = sample_order.car.getCarInfo()['model']
    sample_buyer_last_name = sample_order.buyer.getLastName()
    sample_buyer_first_name = sample_order.buyer.getFirstName()
    sample_employee_str = ' '.join(sample_order.salesBy.__str__().split(" ")[:3])
    expected_output = f"Order #1 {bcolors.BOLD}Made by {sample_employee_str}{bcolors.ENDC}: {sample_car_make} {sample_car_model} for {bcolors.BOLD}{sample_buyer_last_name}, {sample_buyer_first_name}{bcolors.ENDC}"
    assert str(sample_order) == expected_output


def test_eq(sample_order):
    assert sample_order == Order(1, car=mock.MagicMock(), buyer=mock.MagicMock(), dateBought='2022-04-15', employee=mock.MagicMock())
    assert sample_order != 1
    assert sample_order != 'order'
    assert sample_order != mock.MagicMock()
