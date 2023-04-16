from unittest import mock
from parsers import *
from PigeonBox import session, status, orders, users, vehicles

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
    assert interface_objects.ViewByStatus('available') == [vehicles.Car('123456789', 'Camry', 'Toyota', 2021, 25000, 1000, status.Status.AVAILABLE)]
    assert interface_objects.ViewByStatus('sold') == [vehicles.Car('987654321', 'Civic', 'Honda', 2019, 20000, 5000, status.Status.SOLD)]
    assert interface_objects.ViewByStatus('nonexistent') == []
    assert interface_objects.GetInventory() == mock_inventory
    assert interface_objects.searchInventory('Camry', 'Toyota', 2021) == vehicles.Car('123456789', 'Camry', 'Toyota', 2021, 25000, 1000, status.Status.AVAILABLE)
    assert interface_objects.ViewAvailableInventory() == [vehicles.Car('123456789', 'Camry', 'Toyota', 2021, 25000, 1000, status.Status.AVAILABLE)]
    assert interface_objects.UserExists(mock_employee) == True
    assert interface_objects.UserExists(mock_admin) == True
    assert interface_objects.UserExists('emp_username') == True
    assert interface_objects.UsernameExists('emp_username') == True
    assert interface_objects.UsernameExists('non_existing_username') == False
