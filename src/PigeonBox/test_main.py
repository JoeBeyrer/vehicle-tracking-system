import unittest
from unittest.mock import *
from io import *
from PigeonBox.interface import *
from PigeonBox.session import Auth
from PigeonBox.bcolors import *
from PigeonBox.main import *
from PigeonBox.users import *

class TestMain(unittest.TestCase):
    def setUp(self):
        # create a user and interface object for testing
        self.user = User("jdoe123", "password456", "John", "Doe")
        self.interface = Interface()
        self.interface.addUser(self.user)
        self.car = Car(vin='1234567890', info={'make': 'Toyota', 'model': 'Corolla', 'year': 2022, 'mileage': 6},
             performance={'engine': '1.8L 4-cylinder', 'transmission': 'CVT'}, design={'interior': 'black', 'exterior': 'silver'},
             handling=['power steering', 'traction control'], comfort=['air conditioning', 'power windows', 'cruise control'],
             entertainment=['AM/FM radio', 'CD player'], protection={'maintenance': 'basic', 'warranty': ['3-year/36,000-mile basic', '5-year/60,000-mile powertrain']},
             package='standard', status='available', price=20000)
        self.customer = Customer("John", "Doe", "1234-5678-9012-3456", "john.doe@example.com", "1234 1st Ave, Seattle, WA")
        self.employee = Employee("jdoe123", "password456", "John", "Doe")

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
                     
