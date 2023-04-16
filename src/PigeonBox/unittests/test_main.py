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
    
def test_AddCustomer(mocker): #should work - need to add comments
    mock_input = mocker.patch('builtins.input', side_effect=['John', 'Doe', 'johndoe@gmail.com', '4111111111111111', '123 Main St'])
    mock_add_customer = mocker.patch('main.interface.AddCustomer', return_value='John Doe') # 'main.interface.AddCustomer' MAY BE WRONG
    mock_print = mocker.patch('bcolors.PrintFormat')

    result = AddCustomer()
    
    # Check that the mocked functions were called correctly
    mock_input.assert_has_calls([
        mocker.call('First Name'), 
        mocker.call('Last Name'), 
        mocker.call('email address', isEmail=True), 
        mocker.call('Home address')
    ])
    mock_add_customer.assert_called_once_with('John', 'Doe', '4111111111111111', 'johndoe@gmail.com', '123 Main St')
    mock_print.assert_called_once_with('Success', '\nAdded John Doe with success')
    # Check the return value
    assert result == 'John Doe'
    
def test_DeleteCustomerMenu(mocker): # need to comment
    mock_confirm = mocker.patch('main.ConfirmSelection', return_value=True)
    mock_interface = mocker.patch('main.interface.RemoveCustomer')
    mock_print = mocker.patch('main.PrintFormat')

    customer_to_delete = mock.MagicMock(orders=['order1', 'order2'])
    DeleteCustomerMenu(customer_to_delete)

    mock_confirm.assert_called_once_with(
        msg="\nAre you sure you want to delete MagicMock object at",
        title="Confirm Delete",
        cancel=True
    )
    mock_interface.assert_called_once_with(customer_to_delete)
    mock_print.assert_called_once_with("Success", "Removed customer successfully")
    
def test_Login(mocker): # need to comment
    mock_input = mocker.patch('builtins.input', side_effect=['gkubach0', '2nBztx3qzXV'])
    mock_auth = mocker.patch('main.Auth.Authenticate', return_value=mock.MagicMock())
    mock_print = mocker.patch('main.PrintFormat')

    result = Login()

    mock_input.assert_has_calls([
        mocker.call('Enter username: '), 
        mocker.call('Enter password: ')
    ])
    mock_auth.assert_called_once_with('gkubach0', '2nBztx3qzXV')
    mock_print.assert_called_once_with('Important', '\nLogin page')
    assert result is not None
    
    
def test_modifyCarMenu(mocker): #need to comment
    mock_car = mock.MagicMock()
    mock_print = mocker.patch('main.PrintFormat')
    mocker.patch('main.getAction', side_effect=['1', '2', '3', '4'])
    mocker.patch('main.updateCarStatus')
    mocker.patch('main.interface.changeCarPrice')
    mocker.patch('main.interface.changeCarMileage')
    mock_update_warranty = mocker.patch.object(mock_car, 'UpdateWarranty')

    modifyCarMenu(mock_car)

    mock_print.assert_called_once_with('Success', mock_car)
    mock_update_warranty.assert_not_called()

    modifyCarMenu(mock_car)

    mock_print.assert_called_with('Action', mock.ANY)
    mock_update_warranty.assert_not_called()

    modifyCarMenu(mock_car)

    mock_update_warranty.assert_called_once_with(mock.ANY)
    

def test_SearchCarMenu(mocker): # need to comment
    mock_car = mocker.MagicMock()
    mocker.patch('main.CarSearch', return_value=mock_car)
    mocker.patch('main.PrintFormat')
    mocker.patch('main.getAction', side_effect=['1', '2'])

    SearchCarMenu()

    mock_car.getStatusStr.assert_called_once()
    mock_car.UpdateWarranty.assert_not_called()

    SearchCarMenu(mock_car)

    mock_car.getStatusStr.assert_called_once()
    mock_car.UpdateWarranty.assert_not_called()
    
    
def test_InventoryMenu(mocker): # need to comment
    mocker.patch('main.PrintFormat')
    mocker.patch('main.interface.GetInventory', return_value=[])
    mocker.patch('builtins.input', side_effect=['0', '', '1', '', '2', '', '3', '', '4', '', '', '', '', '', '', '', '', '', '', ''])

    InventoryMenu()

    assert main.interface.GetInventory.call_count == 5
    assert main.PrintFormat.call_count == 11
    
    
def test_AddCar(mocker):
    # Mock the input functions
    mocker.patch('builtins.input', side_effect=['12345', 'Ford, Mustang, 2022', '5000, Red', '20000', 'V8, Automatic', 'Leather, Sunroof', 'Metallic', 'Sport', 'Standard', '5, 100000'])
    
    # Mock the interface.AddInventory function to return True
    mocker.patch('main.interface.AddInventory', return_value=True)
    
    # Call the function
    result = main.AddCar()
    
    # Check that the interface.AddInventory function was called with the correct parameters
    main.interface.AddInventory.assert_called_with('12345', info={'model': 'Mustang', 'make': 'Ford', 'mileage': 5000, 'year': 2022, 'color': 'Red'}, performance={'engine': 'V8', 'transmission': 'Automatic'}, comfort=['Standard'], design={'interior': ['Leather'], 'exterior': [{'paint': 'Metallic', 'extra': ['Sunroof']}]}, protection={'maintenance': '100000', 'warranty': ['5']}, price=20000, handling=['Sport'], package='Standard', entertainment=['Sport'], status=mock.ANY)
    
    # Check that the function returns True
    assert result == True
    

def test_RemoveCar(mocker):
    # Mock the necessary dependencies
    inventory_mock = mocker.patch('main.interface.GetInventory')
    inventory_mock.return_value = ['car1', 'car2']
    is_ordered_mock = mocker.patch('main.interface.isCarOrdered')
    is_ordered_mock.return_value = False
    remove_mock = mocker.patch('main.interface.RemoveInventory')
    remove_mock.return_value = True
    print_mock = mocker.patch('builtins.print')

    # Test the function
    RemoveCar()

    # Check that the necessary functions were called
    inventory_mock.assert_called_once()
    is_ordered_mock.assert_called_once_with('car1')
    remove_mock.assert_called_once_with('car1')
    print_mock.assert_called_once_with("Success: Removed car successfully")
    

def test_addOrderMenu(mocker):
    # Mock the necessary dependencies
    print_mock = mocker.patch('builtins.print')
    confirm_mock = mocker.patch('main.ConfirmSelection')
    confirm_mock.side_effect = [True, False]  # Return values for first two ConfirmSelection calls
    add_customer_mock = mocker.patch('main.AddCustomer')
    add_customer_mock.return_value = {'name': 'John Doe', 'email': 'johndoe@example.com'}
    get_object_mock = mocker.patch('main.GetObject')
    get_object_mock.return_value = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    make_order_mock = mocker.patch('main.interface.MakeOrder')
    make_order_mock.return_value = {'order_id': 1234, 'car': 'Tesla Model S', 'customer': 'John Doe'}

    # Test the function
    addOrderMenu('Tesla Model S', [{'name': 'Jane Doe', 'email': 'janedoe@example.com'}])

    # Check that the necessary functions were called
    print_mock.assert_called_with('Success', {'order_id': 1234, 'car': 'Tesla Model S', 'customer': 'John Doe'})
    confirm_mock.assert_called_with(msg='Is this order for a new customer?')
    add_customer_mock.assert_called_once()
    make_order_mock.assert_called_with({'name': 'John Doe', 'email': 'johndoe@example.com'}, 'Tesla Model S', seller='user')
    
def test_OrderMenu(mocker):
    # Mock the necessary dependencies
    print_mock = mocker.patch('builtins.print')
    confirm_mock = mocker.patch('main.ConfirmSelection')
    confirm_mock.side_effect = [False]  # Return value for ConfirmSelection call
    get_action_mock = mocker.patch('main.getAction')
    get_action_mock.side_effect = ["1", ""]  # Return values for getAction calls
    get_object_mock = mocker.patch('main.GetObject')
    get_object_mock.side_effect = [{'model': 'Tesla Model S', 'price': 80000}, None]  # Return values for GetObject calls
    add_order_menu_mock = mocker.patch('main.addOrderMenu')

    # Test the function
    OrderMenu()

    # Check that the necessary functions were called
    print_mock.assert_any_call('Order Menu')
    print_mock.assert_any_call('What would you like to do?')
    get_object_mock.assert_called_with([])
    add_order_menu_mock.assert_called_with({'model': 'Tesla Model S', 'price': 80000}, [])
    confirm_mock.assert_called_once_with(msg='Are you sure you want to remove this order: None?')
    get_object_mock.assert_called_with([])
    
def test_ManageEmployeesMenu(mocker):
    # Mock the necessary dependencies
    print_mock = mocker.patch('builtins.print')
    get_action_mock = mocker.patch('main.getAction')
    get_action_mock.side_effect = ["1", "", "3", "", ""]  # Return values for getAction calls
    get_object_mock = mocker.patch('main.GetObject')
    get_object_mock.side_effect = [Employee(username='johndoe', password='password', first_name='John', last_name='Doe', date_joined=datetime.date(2020, 1, 1)), None]  # Return values for GetObject calls 
    add_employee_mock = mocker.patch('main.AddEmployee')
    remove_employee_menu_mock = mocker.patch('main.RemoveEmployeeMenu')

    # Test the function
    ManageEmployeesMenu()

    # Check that the necessary functions were called
    print_mock.assert_any_call('Employee Management Menu')
    print_mock.assert_any_call('1. View Employee details')
    print_mock.assert_any_call('2. Add Employee')
    print_mock.assert_any_call('3. Remove Employee')
    get_object_mock.assert_called_with([])
    print_mock.assert_called_once_with('Employee: John Doe\nUsername: johndoe\nDate joined: 2020-01-01\n') # Replace the expected employee details
    get_object_mock.assert_called_with([])
    remove_employee_menu_mock.assert_called_once()
    get_object_mock.assert_called_with([])
    add_employee_mock.assert_called_once()
    
    
def test_validateCreditCard(mocker):
    mocker.patch('builtins.input', side_effect=["123456789012345", "1234567890123456"])
    result = validateCreditCard()
    assert result == "1234567890123456"
    
def test_modifyCustomerDetails(mocker):
    # Mock the necessary dependencies
    print_mock = mocker.patch('builtins.print')
    get_action_mock = mocker.patch('main.getAction')
    get_action_mock.side_effect = ["1", "123 Main St", "", "2", "newemail@example.com", "", "3", "4111111111111111", ""]  # Return values for getAction calls
    get_object_mock = mocker.patch('main.GetObject')
    customer_mock = mocker.MagicMock()
    get_object_mock.side_effect = [customer_mock, None]  # Return values for GetObject calls 
    change_customer_address_mock = mocker.patch.object(interface, 'changeCustomerAddress')
    change_customer_email_mock = mocker.patch.object(interface, 'changeCustomerEmail')
    change_customer_card_mock = mocker.patch.object(interface, 'changeCustomerCard')
    email_exists_mock = mocker.patch.object(interface, 'emailExists')
    email_exists_mock.return_value = False
    validate_credit_card_mock = mocker.patch('main.validateCreditCard')
    validate_credit_card_mock.return_value = '4111111111111111'

    # Test the function
    modifyCustomerDetails()

    # Check that the necessary functions were called
    get_object_mock.assert_called_with(interface.getCustomerList())
    print_mock.assert_any_call('1. Update home address')
    print_mock.assert_any_call('2. Update email address')
    print_mock.assert_any_call('3. Update card details')
    get_object_mock.assert_called_with(interface.getCustomerList())
    change_customer_address_mock.assert_called_with(customer_mock, "123 Main St")
    get_object_mock.assert_called_with(interface.getCustomerList())
    email_exists_mock.assert_called_with("newemail@example.com")
    change_customer_email_mock.assert_called_with(customer_mock, "newemail@example.com")
    validate_credit_card_mock.assert_called_once()
    change_customer_card_mock.assert_called_with(customer_mock, '4111111111111111')
    
def test_ManageCustomersMenu(mocker):
    # Mock the necessary dependencies
    print_mock = mocker.patch('builtins.print')
    get_action_mock = mocker.patch('main.getAction')
    #Mock for various user inputs
    get_action_mock.side_effect = ["1", "", "2", "Alice", "Smith", "1111222233334444", "alice@example.com", "123 Main St", "4", "1", "", "n", "3", "Alice", "Smith", "1111222233334444", "alice@example.com", "123 Main St", "2", "Bob", "Jones", "5555666677778888", "bob@example.com", "456 Second St", "", ""]

    get_object_mock = mocker.patch('main.GetObject')
    customer_mock = mocker.MagicMock()
    get_object_mock.side_effect = [customer_mock, None]  # Return values for GetObject calls 

    add_customer_mock = mocker.patch('main.AddCustomer')
    delete_customer_menu_mock = mocker.patch('main.DeleteCustomerMenu')
    modify_customer_details_mock = mocker.patch('main.modifyCustomerDetails')

    # Test the function
    ManageCustomersMenu()

    # Check that the necessary functions were called
    assert print_mock.call_count == 10
    assert get_action_mock.call_count == 7
    assert get_object_mock.call_count == 4
    add_customer_mock.assert_called_once()
    delete_customer_menu_mock.assert_called_once_with(customer_mock)
    modify_customer_details_mock.assert_called_once_with(customer_mock)

def test_AccountSettingsMenu(mocker):
    # Mock the necessary dependencies
    print_mock = mocker.patch('builtins.print')
    get_action_mock = mocker.patch('main.getAction')
    get_action_mock.side_effect = ["1", "", "2", "", "3", ""]

    validate_password_mock = mocker.patch('main.validatePassword')
    validate_password_mock.side_effect = ["new_password", None]

    validate_username_mock = mocker.patch('main.validateUsername')
    validate_username_mock.side_effect = ["new_username", None]

    change_password_menu_mock = mocker.patch('main.ChangePasswordMenu')
    change_username_menu_mock = mocker.patch('main.ChangeUsernameMenu')

    # Test the function
    AccountSettingsMenu()

    # Check that the necessary functions were called
    assert print_mock.call_count == 3
    assert get_action_mock.call_count == 3
    assert validate_password_mock.call_count == 2
    assert validate_username_mock.call_count == 2
    change_password_menu_mock.assert_called_once()
    change_username_menu_mock.assert_called_once()
    
def test_menu(mocker):
    # Mock the necessary dependencies
    print_mock = mocker.patch('builtins.print')
    get_action_mock = mocker.patch('main.getAction')
    get_action_mock.side_effect = ["1", "q", "", "2", "invalid", "3", "4", "invalid", "", "a", "", "q", ""]

    order_menu_mock = mocker.patch('main.OrderMenu')
    car_sales_menu_mock = mocker.patch('main.CarSalesMenu')
    inventory_menu_mock = mocker.patch('main.InventoryMenu')
    manage_customers_menu_mock = mocker.patch('main.ManageCustomersMenu')
    manage_employees_menu_mock = mocker.patch('main.ManageEmployeesMenu')
    account_settings_menu_mock = mocker.patch('main.AccountSettingsMenu')

    # Test the function
    menu()

    # Check that the necessary functions were called
    assert print_mock.call_count == 15
    assert get_action_mock.call_count == 13
    order_menu_mock.assert_called_once()
    car_sales_menu_mock.assert_called_once()
    inventory_menu_mock.assert_called_once()
    manage_customers_menu_mock.assert_called_once()
    manage_employees_menu_mock.assert_not_called()
    account_settings_menu_mock.assert_called_once()
    
def test_run(mocker):
    # Test user login
    user_mock = mocker.MagicMock()
    login_mock = mocker.patch('main.Login')
    login_mock.side_effect = [user_mock, None]

    # Test login confirmation
    confirm_mock = mocker.patch('main.ConfirmSelection')
    confirm_mock.side_effect = [True, False]

    # Test interface creation
    interface_mock = mocker.patch('main.Interface')
    admin_interface_mock = mocker.patch('main.AdminInterface')

    # Test the function with a regular user
    run()
    login_mock.assert_called_with()
    interface_mock.assert_called_with()
    admin_interface_mock.assert_not_called()
    confirm_mock.assert_called_with(msg="Would you like to log in again?")

    # Test the function with an admin user
    user_mock.getCategory.return_value = "admin"
    run()
    login_mock.assert_called_with()
    admin_interface_mock.assert_called_with()
    confirm_mock.assert_called_with(msg="Would you like to log in again?")

    # Test the function when the user logs out and logs back in again
    login_mock.side_effect = [user_mock, user_mock, None]
    confirm_mock.side_effect = [True, False]
    run()
    login_mock.assert_called_with()
    admin_interface_mock.assert_called_with()
    confirm_mock.assert_called_with(msg="Would you like to log in again?")

    # Test the function when the user logs out and cancels the login again process
    login_mock.side_effect = [user_mock, None]
    confirm_mock.side_effect = [True, True]
    run()
    login_mock.assert_called_with()
    interface_mock.assert_called_with()
    admin_interface_mock.assert_not_called()
    confirm_mock.assert_called_with(msg="Would you like to log in again?")
