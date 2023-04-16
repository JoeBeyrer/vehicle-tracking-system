from unittest import mock
from parsers import *
from PigeonBox import session, status, orders, users, vehicles
import pytest
from unittest.mock import MagicMock, patch

def test_InterfaceObjects():
    # Set up objects needed for tests
    mock_inventory = [{'vin': '123456789', 'model': 'Camry', 'make': 'Toyota', 'year': 2021, 'price': 25000, 'mileage': 1000, 'status': 'available'},
                      {'vin': '987654321', 'model': 'Civic', 'make': 'Honda', 'year': 2019, 'price': 20000, 'mileage': 5000, 'status': 'sold'}]
    mock_customers = [{'name': 'John Smith', 'email': 'john.smith@example.com', 'card': '1234 5678 9012 3456', 'address': '123 Main St', 'orders': []},
                      {'name': 'Jane Doe', 'email': 'jane.doe@example.com', 'card': '0987 6543 2109 8765', 'address': '456 Oak St', 'orders': []}]
    mock_employee = users.Employee('emp_username', 'emp_password')
    mock_admin = users.Admin('admin_username', 'admin_password')
    mock_users = [mock_employee, mock_admin]

    # Create the InterfaceObjects object
    interface_objects = InterfaceObjects()
    interface_objects.inventory = mock_inventory
    interface_objects.customers = mock_customers
    interface_objects.__users__ = mock_users

    # Test the methods of InterfaceObjects()
    assert interface_objects.usernameToUser('emp_username') == mock_employee
    assert interface_objects.usernameToUser('admin_username') == mock_admin
    assert interface_objects.vinToCar('123456789') == vehicles.Car('123456789', 'Camry', 'Toyota', 2021, 25000, 1000, status.Status.AVAILABLE)
    assert interface_objects.vinToCar('987654321') == vehicles.Car('987654321', 'Civic', 'Honda', 2019, 20000, 5000, status.Status.SOLD)
    assert interface_objects.emailToCustomer('john.smith@example.com') == mock_customers[0]
    assert interface_objects.emailToCustomer('jane.doe@example.com') == mock_customers[1]
    assert interface_objects.getCustomerList() == mock_customers
    assert interface_objects.getEmployeeList() == [mock_employee]
    assert interface_objects.isEmployee(mock_employee) == True
    assert interface_objects.ViewUsers() == mock_users
    assert interface_objects.vinExists('123456789') == True
    assert interface_objects.vinExists('123') == False
    assert interface_objects.inInventory('123456789') == True
    assert interface_objects.inInventory('123') == False
    

# Define a fixture to initialize the Interface object for each test
@pytest.fixture
def interface():
    return Interface()

def test_changeCarStatus(interface, mocker):
    # Create a mock car object
    car = mocker.MagicMock()
    # Call the method being tested
    interface.changeCarStatus(car, "sold")
    # Check that the car's status was updated
    assert car.SetStatus.called_with("sold")
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[0] == True

def test_changeCarPrice(interface, mocker):
    # Create a mock car object
    car = mocker.MagicMock()
    # Call the method being tested
    interface.changeCarPrice(car, 15000)
    # Check that the car's price was updated
    assert car.UpdatePrice.called_with(15000)
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[0] == True

def test_changeCarMileage(interface, mocker):
    # Create a mock car object
    car = mocker.MagicMock()
    # Call the method being tested
    interface.changeCarMileage(car, 10000)
    # Check that the car's mileage was updated
    assert car.UpdateMileage.called_with(10000)
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[0] == True

def test_changeCustomerEmail(interface, mocker):
    # Create a mock customer object
    customer = mocker.MagicMock()
    # Call the method being tested
    interface.changeCustomerEmail(customer, "new_email@example.com")
    # Check that the customer's email was updated
    assert customer.setEmail.called_with("new_email@example.com")
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[3] == True

def test_changeCustomerCard(interface, mocker):
    # Create a mock customer object
    customer = mocker.MagicMock()
    # Call the method being tested
    interface.changeCustomerCard(customer, "new_card_number")
    # Check that the customer's card number was updated
    assert customer.setCard.called_with("new_card_number")
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[3] == True

def test_changeCustomerAddress(interface, mocker):
    # Create a mock customer object
    customer = mocker.MagicMock()
    # Call the method being tested
    interface.changeCustomerAddress(customer, "123 Main St")
    # Check that the customer's address was updated
    assert customer.setAddress.called_with("123 Main St")
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[3] == True

def test_changeUserPassword_admin(interface, mocker):
    # Create a mock admin object
    admin = mocker.MagicMock()
    # Set up the mock interface object with the admin
    interface.admins = [admin]
    # Call the method being tested
    interface.changeUserPassword(admin, "new_password")
    # Check that the admin's password was updated
    assert admin.UpdatePassword.called_with("new_password")
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[2] == True
    
def test_changeUserPassword_employee(interface, mocker):
    # Create a mock employee object
    employee = mocker.MagicMock()
    # Set up the mock interface object with the employee
    interface.employees = [employee]
    # Call the method being tested
    interface.changeUserPassword(employee, "new_password")
    # Check that the admin's password was updated
    assert admin.UpdatePassword.called_with("new_password")
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[2] == True
    
def test_changeUserUsername_admin(interface, mocker):
    # Create a mock admin object
    admin = mocker.MagicMock()
    # Set up the mock interface object with the admin
    interface.admins = [admin]
    # Call the method being tested
    interface.changeUserUsername(admin, "new_Username")
    # Check that the admin's password was updated
    assert admin.UpdateUsername.called_with("new_Username")
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[2] == True
    
def test_changeUserUsername_employee(interface, mocker):
    # Create a mock employee object
    employee = mocker.MagicMock()
    # Set up the mock interface object with the employee
    interface.employees = [employee]
    # Call the method being tested
    interface.changeUserUsername(employee, "new_Username")
    # Check that the admin's password was updated
    assert admin.UpdateUsername.called_with("new_Username")
    # Check that the isObjListUpdated flag was set to True
    assert interface.isObjListUpdated[2] == True
    
def test_isCarOrdered(interface, mocker):
    # Create mock objects for car and order
    car = mocker.MagicMock()
    order = mocker.MagicMock()
    # Set up order object to return the mock car object
    order.getCar.return_value = car
    # Set up the mock interface object with the order
    interface.orders = [order]
    # Check that the method returns True for a matching car
    assert interface.isCarOrdered(car) == True
    # Check that the method returns False for a non-matching car
    assert interface.isCarOrdered(mocker.MagicMock()) == False

def test_doesOrderExist(interface, mocker):
    # Create mock objects for order
    order1 = mocker.MagicMock()
    order2 = mocker.MagicMock()
    # Set up the mock interface object with one of the orders
    interface.orders = [order1]
    # Check that the method returns True for an existing order
    assert interface.doesOrderExist(order1) == True
    # Check that the method returns False for a non-existing order
    assert interface.doesOrderExist(order2) == False

def test_MakeOrder(interface, mocker):
    # Create mock objects for the customer, vehicle, and seller
    customer = mocker.MagicMock()
    vehicle1 = mocker.MagicMock()
    vehicle1.isAvailable.return_value = True
    vehicle2 = mocker.MagicMock()
    vehicle2.isAvailable.return_value = False
    seller = mocker.MagicMock()
    # Check that a new order was added to the interface's list of orders when vehicle is available
    interface.MakeOrder(customer, vehicle1, seller)
    assert len(interface.orders) == 1
    # Check that no new order was added to the interface's list of orders when vehicle is unavailable
    interface.MakeOrder(customer, vehicle2, seller)
    assert len(interface.orders) == 1
    
def test_UndoOrder(interface, mocker):
    # Create a mock order object and add it to the interface's orders list
    order = mocker.MagicMock()
    interface.orders = [order]
    
    # Call the method being tested
    interface.UndoOrder(order)
    
    # Check that the order was removed from the orders list
    assert order not in interface.orders
    
    # Check that the order's RemoveOrder method was called
    order.RemoveOrder.assert_called_once()
    
    # Check that the order object was deleted
    assert mocker.call.del(order) in mocker.spy(interface, 'del').call_args_list
    
    # Check that the isObjListUpdated flag was set to True for orders
    assert interface.isObjListUpdated[1] == True


def test_emailExists(interface, mocker):
    # Create a mock customer object with a given email
    email = "test@example.com"
    customer = mocker.MagicMock()
    customer.getEmail.return_value = email
    
    # Set up the mock interface object with the customer
    interface.customers = [customer]
    
    # Test with an existing email
    result = interface.emailExists(email)
    assert result == True
    
    # Test with a non-existing email
    result = interface.emailExists("different@example.com")
    assert result == False


def test_isCustomer(interface, mocker):
    # Create a mock customer object and add it to the interface's customers list
    customer = mocker.MagicMock()
    interface.customers = [customer]
    
    # Test with the customer object
    result = interface.isCustomer(customer)
    assert result == True
    
    # Test with a non-existing customer object
    result = interface.isCustomer(mocker.MagicMock())
    assert result == False


def test_AddCustomer(interface, mocker):
    # Create a mock customer object
    customer = mocker.MagicMock()
    customer.getEmail.return_value = "test@example.com"
    
    # Test with a non-existing email
    interface.customers = []
    result = interface.AddCustomer("John", "Doe", "123", "test@example.com", "123 Main St")
    assert result == customer
    assert customer in interface.customers
    
    # Test with an existing email
    interface.customers = [customer]
    result = interface.AddCustomer("Jane", "Doe", "456", "test@example.com", "456 Main St")
    assert result == None
    assert len(interface.customers) == 1
    
def test_RemoveCustomer(interface, mocker):
    # Create a mock customer and order objects
    customer = mocker.MagicMock()
    order1 = mocker.MagicMock()
    order2 = mocker.MagicMock()
    # Set up the mock interface object with the customer and orders
    interface.customers = [customer]
    interface.orders = [order1, order2]
    order1.getUser.return_value = customer
    order2.getUser.return_value = customer
    order1.getCar.getStatus.return_value = status.Status.DELIVERED
    order2.getCar.getStatus.return_value = status.Status.ORDERED
    # Call the method being tested
    interface.RemoveCustomer(customer)
    # Check that the customer was removed from the customers list
    assert len(interface.customers) == 0
    # Check that the customer object was deleted
    mocker.spy(interface, 'del')
    interface.del(customer)
    assert interface.del.called_once_with(customer)
    # Check that the isObjListUpdated flag was set to True for customers
    assert interface.isObjListUpdated[3] == True
    # Check that the orders for the customer were removed from the orders list
    assert len(interface.orders) == 0
    # Check that the UndoOrder method was called for each order
    order1.RemoveOrder.assert_called_once()
    order2.RemoveOrder.assert_called_once()
    # Check that the car status was updated for the delivered order
    assert order1.getCar.setStatus.called_once_with(status.Status.BACKORDER)
    

def test_LogOut(interface, mocker):
    # Set up the mock interface object with updated flags
    interface.isObjListUpdated = [True, False, True, False]
    # Call the method being tested
    interface.LogOut()
    # Check that the writeJson method was called for the updated lists
    writeJson.writeJson.assert_any_call(interface.inventory)
    writeJson.writeJson.assert_any_call(interface.customers)
    allUsers = interface.admins + interface.employees
    writeJson.writeJson.assert_any_call(allUsers)
    # Check that the writeJson method was not called for the non-updated list
    writeJson.writeJson.assert_not_called(interface.orders)
