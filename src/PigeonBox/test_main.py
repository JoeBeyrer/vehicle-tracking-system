import io
import pytest
from PigeonBox.interface import *
from PigeonBox.session import Auth
from PigeonBox.bcolors import *
from PigeonBox.main import *
from PigeonBox.users import *


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



