import io
import pytest
from PigeonBox.interface import *
from PigeonBox.session import Auth
from PigeonBox.bcolors import *
from PigeonBox.main import *
from PigeonBox.users import *
from unittest.mock import *



def test_displayData(mocker):
    # create a list of test data
    data = ["apple", "banana", "cherry"]

    # capture the printed output of displayData
    with mocker.patch('sys.stdout', new=io.StringIO()) as fake_out:
        displayData(data)

    # assert that the printed output is correct
    assert fake_out.getvalue() == "0: apple\n1: banana\n2: cherry\n"


def test_isEmpty():
    # test with an empty list
    assert isEmpty([]) == True

    # test with a non-empty list
    assert isEmpty([1, 2, 3]) == False


def test_validatePassword(mocker):
    # mock the ValidateUserInput function to return "password" for both prompts
    mocker.patch.object(main, 'ValidateUserInput', side_effect=["password", "password"])

    # test with matching passwords
    assert validatePassword() == "password"

    # mock the ValidateUserInput function to return "password" for the first prompt
    mocker.patch.object(main, 'ValidateUserInput', side_effect=["password", None])

    # test with non-matching passwords
    assert validatePassword() == None


def test_validateUsername(mocker):
    # mock the ValidateUserInput function to return "newusername" for the prompt
    mocker.patch.object(main, 'ValidateUserInput', return_value="newusername")

    # test with a unique username
    assert validateUsername() == "newusername"

    '''
    # test with a non-unique username
    interface.addUser(User("newusername", "password"))
    mocker.patch.object(main, 'ValidateUserInput', return_value="newusername")
    assert validateUsername() == None
    '''


def test_ConfirmSelection(mocker):
    # mock the input function to return "y"
    mocker.patch.object(builtins, 'input', return_value="y")
    assert ConfirmSelection() == True

    # mock the input function to return "n"
    mocker.patch.object(builtins, 'input', return_value="n")
    assert ConfirmSelection() == False


def test_ValidateUserInput(mocker):
    # mock the input function to return "1"
    mocker.patch.object(builtins, 'input', return_value="1")

    # test with isNum=True
    assert ValidateUserInput(isNum=True) == 1

    # mock the input function to return "user@example"
    mocker.patch.object(builtins, 'input', return_value="user@example")

    # test with isEmail=True
    assert ValidateUserInput(isEmail=True) == "user@example"

    # mock the input function to return "badinput", "", "2"
    mocker.patch.object(builtins, 'input', side_effect=["badinput", "", "2"])

    # test with default options
    assert ValidateUserInput() == "2"


def test_getAction(mocker):
    # mock the input function to return "1"
    mocker.patch.object(builtins, 'input', return_value="1")
    assert getAction() == "1"

    # mock the input function to return "invalid", "2"
    mocker.patch.object(builtins, 'input', side_effect=["invalid", "2"])
    assert getAction() == "2"
    

def test_PickIndex(mocker):
    # test with an empty list
    mocker.patch.object(builtins, 'input', return_value='q')
    assert PickIndex([]) == None
    
    # test with a non-empty list
    mocker.patch.object(builtins, 'input', side_effect=['a', '2', '1'])
    assert PickIndex(['apple', 'banana', 'cherry']) == 1

    # test with an index out of bounds
    mocker.patch.object(builtins, 'input', side_effect=['5', '-1', '0', 'q'])
    assert PickIndex(['apple', 'banana', 'cherry']) == None

    # test with a non-numeric input
    mocker.patch.object(builtins, 'input', side_effect=['one', '0', 'q'])
    assert PickIndex(['apple', 'banana', 'cherry']) == None

    # test with cancelling
    mocker.patch.object(builtins, 'input', return_value='q')
    assert PickIndex(['apple', 'banana', 'cherry']) == None

    
def test_SeparateInputToList():
    # test with a single item
    assert SeparateInputToList("apple") == ["apple"]

    # test with multiple items separated by comma
    assert SeparateInputToList("apple, banana, cherry") == ["apple", "banana", "cherry"]

    # test with multiple items separated by comma and whitespace
    assert SeparateInputToList("apple,     banana, cherry") == ["apple", "banana", "cherry"]

    # test with no input
    assert SeparateInputToList("") == []
    
    
def test_GetObject(mocker):
    # mock the PickIndex function to return 1
    mocker.patch.object(main, 'PickIndex', return_value=1)

    # create a list of test data
    data = ["apple", "banana", "cherry"]

    # test with a valid index
    assert GetObject(data) == "banana"

    # mock the PickIndex function to return None
    mocker.patch.object(main, 'PickIndex', return_value=None)

    # test when the user exits
    assert GetObject(data) == None
    
    
def test_updateCarStatus(): #MAY BE WRONG -- could be too simple of a test, but it strictly tests functionality, no integration so should be ok
    # define initial car status
    car = {'make': 'Honda', 'model': 'Civic', 'year': 2022, 'status': 'available'}

    # simulate user choosing new status "ordered"
    statusChoice = "1"

    # call updateCarStatus function with car object and new status choice
    updateCarStatus(car, statusChoice)

    # check that car status has been updated to "ordered"
    assert car['status'] == "ordered"

    # check that success message was printed with updated car object
    assert "Success" in captured_output.getvalue()
    assert str(car) in captured_output.getvalue()

def test_AddEmployee(mocker): #MAY BE WRONG
    # Mocking user inputs
    mocker.patch('main.ValidateUserInput', side_effect=["test_username", "test_password", "John", "Doe"])

    # Mocking ConfirmSelection to return False
    mocker.patch('main.ConfirmSelection', return_value=False)

    # Mocking AddEmployee method to return False
    interface_mock = MagicMock()
    interface_mock.AddEmployee.return_value = False
    mocker.patch('interface', interface_mock) # maybe interface.Interface??

    # Assert that the function prints failure message when employee is not added
    assert AddEmployee() == PrintFormat("Invalid", "User ('John', 'Doe') already exists")

def test_RemoveEmployeeMenu(mocker):
    # Set up the mocker
    interface = mocker.MagicMock()
    interface.getEmployeeList.return_value = ["Alice", "Bob", "Charlie"]
    interface.RemoveUser.return_value = True

    # Set up the input for the user's selection
    mocker.patch("builtins.input", side_effect=["1", "yes"])

    # Call the function
    RemoveEmployeeMenu()

    # Check that the correct methods were called and that the correct output was printed
    interface.getEmployeeList.assert_called_once()
    interface.RemoveUser.assert_called_with("Bob")
    assert "Removed employee successfully" in mocker.call.print.call_args_list[0][0][1]
    
def test_displayStatusOptions(mocker): #MAY BE WRONG
    # Mock the displayData and getAction functions
    display_data_mock = mocker.patch("module_name.displayData")
    get_action_mock = mocker.patch("module_name.getAction", return_value="0")

    # Call the function under test
    result = displayStatusOptions()

    # Check that displayData was called with the correct argument
    display_data_mock.assert_called_once_with(["Available", "Ordered", "BackOrder", "Delivered"])

    # Check that getAction was called with the correct argument
    get_action_mock.assert_called_once_with({"0", "1", "2", "3"}, msg="Pick a status:")

    # Check that the function returns the expected value
    assert result == "0"
    
def test_CarSearch(mocker): # should work
    # Mocking user input
    mocker.patch('builtins.input', return_value='Civic,Honda,2015')

    # Mocking searchInventory method to return a car
    interface_mock = MagicMock()
    car_mock = MagicMock()
    car_mock.getDetails.return_value = 'Civic, Honda, 2015'
    interface_mock.searchInventory.return_value = car_mock
    mocker.patch('interface', interface_mock) # maybe interface.Interface???

    # Assert that the function returns the correct car details when a car is found
    assert CarSearch() == car_mock
    assert interface_mock.searchInventory.called_with('Civic', 'Honda', 2015)

    # Mocking searchInventory method to return None
    interface_mock.searchInventory.return_value = None

    # Assert that the function prints 'No car match' message when no car is found
    assert CarSearch() is None
    assert interface_mock.searchInventory.called_with('Civic', 'Honda', 2015)

def test_filterByMenu(mocker):
    # Mocking user input
    mocker.patch('builtins.input', return_value='1')

    # Mocking ViewByStatus method to return a list of cars
    interface_mock = mocker.MagicMock()
    interface_mock.ViewByStatus.return_value = ['Car 1', 'Car 2']
    mocker.patch('interface', interface_mock) # maybe interface.Interface???

    # Assert that the function calls the ViewByStatus method with the correct status and returns None
    assert filterByMenu() is None
    interface_mock.ViewByStatus.assert_called_once_with('available')

    # Mocking user input with an invalid option
    mocker.patch('builtins.input', return_value='invalid_option')

    # Assert that the function returns None when an invalid option is entered
    assert filterByMenu() is None

def test_modifyInventoryMenu(mocker):
    # Mock isAdmin to True
    mocker.patch('isAdmin', True) # may need main.isAdmin

    # Mock user input for selecting 'Add car' option
    mocker.patch('builtins.input', return_value='1')

    # Mock AddCar method to return None
    mocker.patch('main.AddCar', return_value=None)

    # Assert that the function calls the AddCar method and returns None
    assert modifyInventoryMenu() is None
    main.AddCar.assert_called_once()

    # Mock user input for selecting 'Remove car' option
    mocker.patch('builtins.input', return_value='2')

    # Mock RemoveCar method to return None
    mocker.patch('main.RemoveCar', return_value=None)

    # Assert that the function calls the RemoveCar method and returns None
    assert modifyInventoryMenu() is None
    main.RemoveCar.assert_called_once()
