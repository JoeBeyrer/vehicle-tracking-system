import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from PigeonBox.interface import User, Interface
from PigeonBox.session import Auth
from main import *

class TestMain(unittest.TestCase):
    def setUp(self):
        # create a user and interface object for testing
        self.user = User("testuser", "password")
        self.interface = Interface()
        self.interface.addUser(self.user)
        self.car = main.Car("Tesla", "Model S", 2021, "ABC123")
        self.customer = main.Customer("John", "Doe", "john.doe@example.com", "1234 1st Ave, Seattle, WA", "1234-5678-9012-3456")
        self.employee = main.Employee("jdoe", "password", "John", "Doe")

    def test_displayData(self):
        # create a list of test data
        data = ["apple", "banana", "cherry"]

        # capture the printed output of displayData
        with patch('sys.stdout', new=StringIO()) as fake_out:
            displayData(data)

        # assert that the printed output is correct
        self.assertEqual(fake_out.getvalue(), "0: apple\n1: banana\n2: cherry\n")

    def test_isEmpty(self):
        # test with an empty list
        self.assertTrue(isEmpty([]))

        # test with a non-empty list
        self.assertFalse(isEmpty([1, 2, 3]))

    def test_validatePassword(self):
        # mock the ValidateUserInput function to return "password" for both prompts
        with patch('main.ValidateUserInput', side_effect=["password", "password"]):
            # test with matching passwords
            self.assertEqual(validatePassword(), "password")

        # mock the ValidateUserInput function to return "password" for the first prompt
        with patch('main.ValidateUserInput', side_effect=["password", None]):
            # test with non-matching passwords
            self.assertIsNone(validatePassword())

    def test_validateUsername(self):
        # mock the ValidateUserInput function to return "newusername" for the prompt
        with patch('main.ValidateUserInput', return_value="newusername"):
            # test with a unique username
            self.assertEqual(validateUsername(), "newusername")

        # test with a non-unique username
        self.interface.addUser(User("newusername", "password"))
        with patch('main.ValidateUserInput', return_value="newusername"):
            self.assertIsNone(validateUsername())

    def test_ConfirmSelection(self):
        # mock the input function to return "y"
        with patch('builtins.input', return_value="y"):
            self.assertTrue(ConfirmSelection())

        # mock the input function to return "n"
        with patch('builtins.input', return_value="n"):
            self.assertFalse(ConfirmSelection())

    def test_ValidateUserInput(self):
        # mock the input function to return "1"
        with patch('builtins.input', return_value="1"):
            # test with isNum=True
            self.assertEqual(ValidateUserInput(isNum=True), 1)

        # mock the input function to return "user@example"
        with patch('builtins.input', return_value="user@example"):
            # test with isEmail=True
            self.assertEqual(ValidateUserInput(isEmail=True), "user@example")

        # mock the input function to return "badinput", "", "2"
        with patch('builtins.input', side_effect=["badinput", "", "2"]):
            # test with default options
            self.assertEqual(ValidateUserInput(), "2")

    def test_getAction(self):
        # mock the input function to return "1"
        with patch('builtins.input', return_value="1"):
            self.assertEqual(getAction(), "1")

        # mock the input function to return "invalid", "2"
        with patch('builtins.input', side_effect=["invalid", "2"]):
            self.assertEqual
                     
            
    @patch('builtins.input', side_effect=['1', 'Tesla', 'Model S', '2021', 'ABC123', '100'])
    def test_add_car(self, mock_input):
        main.AddCar()
        inventory = main.interface.getInventory()
        self.assertEqual(len(inventory), 1)
        self.assertEqual(inventory[0].getModel(), "Model S")

    @patch('builtins.input', side_effect=['john', 'password', 'John', 'Doe'])
    def test_add_employee(self, mock_input):
        main.AddEmployee()
        employees = main.interface.getEmployeeList()
        self.assertEqual(len(employees), 2)
        self.assertEqual(employees[1].getUsername(), "jdoe")

    @patch('builtins.input', side_effect=['1', 'jdoe', 'password'])
    def test_login_employee(self, mock_input):
        employee = main.Login()
        self.assertEqual(employee.getUsername(), "jdoe")

    @patch('builtins.input', side_effect=['John', 'Doe', 'john.doe@example.com', '1234 1st Ave, Seattle, WA', '1234-5678-9012-3456'])
    def test_add_customer(self, mock_input):
        main.AddCustomer()
        customers = main.interface.getCustomerList()
        self.assertEqual(len(customers), 2)
        self.assertEqual(customers[1].getEmail(), "john.doe@example.com")

    @patch('builtins.input', side_effect=['y'])
    def test_remove_employee(self, mock_input):
        main.RemoveEmployee()
        employees = main.interface.getEmployeeList()
        self.assertEqual(len(employees), 1)

    @patch('builtins.input', side_effect=['John', 'Doe', 'john.doe@example.com', '1234 1st Ave, Seattle, WA', '1234-5678-9012-3456'])
    def test_remove_customer(self, mock_input):
        main.DeleteCustomer(self.customer)
        customers = main.interface.getCustomerList()
        self.assertEqual(len(customers), 1)

    @patch('builtins.input', side_effect=['1', 'Tesla,Model S,2021', '2', '3', '2', '5'])
    def test_modify_inventory(self, mock_input):
        main.modifyInventoryMenu()
        inventory = main.interface.getInventory()
        self.assertEqual(len(inventory), 0)

    @patch('builtins.input', side_effect=['1', 'Tesla,Model S,2021', '2', '3', '2', '5'])
    def test_modify_inventory_non_admin(self, mock_input):
        main.isAdmin = False
        main.modifyInventoryMenu()
        inventory = main.interface.getInventory()
        self.assertEqual(len(inventory), 0)
        main.isAdmin = True

    @patch('builtins.input', side_effect=['1', '1000', '100', '2022-05-01', '2022-05-05', 'john'])
