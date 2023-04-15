from PigeonBox.interface import *
from PigeonBox.session import Auth
from PigeonBox.bcolors import *

'''fortest'''
''' Command line interface '''
def displayData(data):
    """ Given an array, display each element in the array along with the index"""
    if isEmpty(data): return

    for i, val in enumerate(data):
        print(f"{i}: {val}")

def StallUntilUserInput():
    """ Stalls the program, waits for user to press enter, 
    to let them view whatever output was printed post an action"""
    input(f"{bcolors.HEADER}\nPress any key to continue {bcolors.ENDC}")

def isEmpty(arr):
    if not arr:
        PrintFormat("Warning", "No data to display")
        return True
    return False


def validatePassword():
    newPassword = ValidateUserInput('new password')
    if not newPassword: return
    confirmPassword = ValidateUserInput('confirm password')
    if not confirmPassword: return

    if confirmPassword != newPassword:
        PrintFormat("Invalid", "Passwords do not match")
        return

    if newPassword == user.getPassword():
        PrintFormat("Invalid", "New password cannot be the same as old password")
        return
    
    return newPassword

''' User account details'''
def ChangePasswordMenu():
    newPassword = validatePassword()
    if not newPassword: return
    interface.changeUserPassword(user, newPassword)
    PrintFormat("Success", "Password changed successfully")

def validateUsername():
    newUsername = ValidateUserInput('new username')
    if not newUsername: return
    if newUsername == user.getUsername():
        PrintFormat("Invalid", "New username cannot be the same as old username")
        return
    
    for usr in interface.ViewUsers():
        if usr.getUsername() == newUsername:
            PrintFormat("Invalid", "Username already taken")
            return
    return newUsername
def ChangeUsernameMenu():
    newUsername = validateUsername()
    if not newUsername: return
    interface.changeUserUsername(user, newUsername)
    PrintFormat("Success", "Username changed successfully")

''' Checkers and validators '''
def ConfirmSelection(response = {"y", "yes"}, msg="") -> bool:
    if not msg: msg = "\nAre you sure you want to proceed?"
    PrintFormat("Warning", msg)
    confirm = input("Enter [y/n] to confirm: ")
    if confirm.lower() not in response:
        return False
    PrintFormat("Success", "Action confirmed")
    return True

def ValidateUserInput(action="action", isNum=False, isEmail=False):
    PrintFormat("Important", "\nPress 'q' to exit")
    while True:
        userInput = input(f"Enter {action}: ")
        if userInput.lower() == 'q':
            PrintFormat("Warning", "Exitting\n")
            return
        if not userInput: 
            PrintFormat("Invalid", "Bad input")
            continue
        if isNum and (not userInput.isdigit()):
            PrintFormat("Invalid", "Must be a number")
            continue
        if isEmail and ("@" not in userInput or "." not in userInput):
            PrintFormat("Invalid", "Must be a valid email address")
            continue

        PrintFormat("Success", userInput)
        return int(userInput) if isNum else userInput

''' General helper functions '''
def getAction(validSet={"1", "2", "3"}, msg="Enter action:"):
    PrintFormat("Important", "\nPress 'q' to exit")
    action = input(f"{bcolors.UNDERLINE}{msg}{bcolors.ENDC} ").lower()
    if action == "q":
        PrintFormat("Warning", "Exitting\n")
        return
    if action not in validSet:
        PrintFormat("Invalid", "Invalid action")
        return getAction(validSet, msg)
    return action

def PickIndex(arr):
    """  Will display elements in array and ask user to pick one, will return the index of the element picked
        Useful for when choosing an element to view or remove. Like when removing a car, this will point to its index in the list
        and the user will be able to remove it by index."""
    arrLength = len(arr) - 1 # length to give user bounds to pick from
    while True:
        displayData(arr) # displays with (index: element) pair
        PrintFormat('Action', '\nPick index from the dislayed list above')
        index = input(f"Enter index [0-{arrLength}] OR enter 'q' to exit: ")
        if index == 'q': 
            PrintFormat("Warning", "Exitting\n")
            return # exitting
        
        # validation
        if not index.isdigit():
            PrintFormat('Invalid',f"Invalid index! Must be a number")
            StallUntilUserInput()
            continue

        index = int(index)
        if index < 0 or index > arrLength:
            PrintFormat('Invalid',f"Invalid index! Must be greater than 0 AND smaller than maximum length")
            StallUntilUserInput()
            continue

        return index
    
def SeparateInputToList(inpt):
    """ Takes in a string and returns an array of the string separated by commas"""
    inpt = inpt.split(',')
    inpt = list(map(lambda x: x.strip(), inpt))
    return inpt

def GetObject(objectList):
    """ selects and returns an object once user chooses it from a list (calls on PickIndex)"""
    index = PickIndex(objectList)
    if index is None: return # exitting

    object = objectList[index]
    PrintFormat('Success',f"\nPicked: {object}") # success message for user
    return object

def updateCarStatus(car):
    statuses = {"0": "available", "1": "ordered", "2": "backorder", "3": "delivered"}
    statusChoice = displayStatusOptions()
    if not statusChoice: return
    car.SetStatus(statuses[statusChoice])
    PrintFormat("Success", f"{car}")
    
''' helper menus'''
def AddEmployee():
    username = ValidateUserInput("Enter username")
    if not username: return
    password = ValidateUserInput(f"Enter password for new user {username}")
    if not password: return
    firstName = ValidateUserInput("Enter first name")
    if not firstName: return
    lastName = ValidateUserInput("Enter last name")
    if not lastName: return
    addEmployee = None
    confirmMessage = f"Do you wish to grant Admin priviledges to {firstName}?"

    if ConfirmSelection(msg=confirmMessage):
        addEmployee = interface.AddAdmin(username, password, firstName, lastName)
    else:
        addEmployee = interface.AddEmployee(username, password, firstName, lastName)
    # check if employee was added and notify user
    if not addEmployee:
        PrintFormat("Invalid", f"User {firstName, lastName} already exists")
        return
    PrintFormat("Success", f"User {firstName, lastName} successfully added")

def RemoveEmployee():
    """ 'Menu' for removing an employee, will ask user to pick from a list of employees
    and then confirm the selection. If the user confirms, the employee will be removed"""
    employeeToDelete = GetObject(interface.getEmployeeList()) # select employee to delete
    confirmMessage = f"\nAre you sure you want to delete {employeeToDelete}"
    if not ConfirmSelection(msg=confirmMessage): 
        return
    
    isRemoved = interface.RemoveUser(employeeToDelete) # remove employee
    if not isRemoved: # check if employee was removed and notify user
        PrintFormat("Invalid", "Employee not found")

    PrintFormat("Success", "Removed employee successfully")


def displayStatusOptions():
    options = ["Available", 
               "Ordered", 
               "BackOrder", 
               "Delivered"]
    displayData(options)
    action = getAction({"0","1","2","3"}, msg="Pick a status:")
    if not action: return
    return action

def CarSearch():
    print('\nSearch car in inventory')
    searchMessage = "Enter model, make and year separated by commas\n"
    searchDecision = SeparateInputToList(input(searchMessage))
    if len(searchDecision) != 3: 
        PrintFormat('Invalid', '\nCar not found, make sure you entered the correct model, make and year')
        return

    model, make, year = searchDecision[0], searchDecision[1], searchDecision[2]
    # validate input
    if not year.isdigit(): 
        PrintFormat('Invalid', '\nYear must be a number!')
        return

    car = interface.searchInventory(model, make, int(year))
    # check car exists
    if not car: 
        PrintFormat('Invalid', '\nNo car match :(')
        return
    
    PrintFormat('Success', f"\nCar details:\n{car.getDetails()}")
    return car

def filterByMenu():
    filterOptions = ["Filter by Status:",
                     "1. Available",
                     "2. Ordered",
                     "3. Backorder",
                     "4. Delivered"]
    displayFilterOptions = "\n" + "\n".join(filterOptions)
    PrintFormat("Action", displayFilterOptions)
    statuses = {"1": "available", "2": "ordered", "3": "backorder", "4": "delivered"}
    filterDecision = getAction(validSet=set(statuses.keys()))
    # validate input
    if not filterDecision: return

    {"1": displayData,
    "2": displayData,
    "3": displayData,
    "4": displayData}[filterDecision](interface.ViewByStatus(statuses[filterDecision]))

def modifyInventoryMenu():
    if not isAdmin: return

    modifyCarOptions = ["1. Add car","2. Remove car"]
    formattedOptions ="\n".join(modifyCarOptions)
    PrintFormat("Action", formattedOptions)
    modifyChoice = getAction(validSet={"1","2"})
    if not modifyChoice: return

    if modifyChoice == '1': 
        AddCar()
        return
    
    RemoveCar()

''' Customer Management helper functions'''
def AddCustomer():
    PrintFormat("Important", "\nEnter customer details\n")
    firstName = ValidateUserInput("First Name")
    if not firstName: return
    lastName = ValidateUserInput("Last Name")
    if not lastName: return
    emailAddress = ValidateUserInput("email address", isEmail=True)
    if not emailAddress: return
    creditCard = validateCreditCard()
    if not creditCard: return
    homeAddress = ValidateUserInput("Home address")
    if not homeAddress: return
    customer = interface.AddCustomer(firstName, lastName, creditCard, emailAddress, homeAddress)
    if not customer: 
        PrintFormat("Invalid", "Customer already exists or email already exists")
        return

    PrintFormat('Success',f"\nAdded {customer} with success")
    return customer

def DeleteCustomer(customerToDelete):
    confirmMessage = f"\nAre you sure you want to delete {customerToDelete}"
    if not ConfirmSelection(msg=confirmMessage): return
    interface.RemoveCustomer(customerToDelete)
    PrintFormat("Success", "Removed customer successfully")

''' Main menus '''
def Login():
    """ This function takes care of the login page,
      it will ask for username and password and will return the user object if the user is authenticated"""
    PrintFormat("Important", "\nLogin page")
    PrintFormat("Important", "\nWelcome to PigeonBox")
    user, attempt = None, 0
    # give the user 3 attempts to get the correct username and password
    while (user is None and attempt < 3):
        attempt+=1
        if attempt > 1:
            PrintFormat("Warning",f"\nAttempt {attempt}")
        # Employee: gkubach0 2nBztx3qzXV
        # crapinett1 KcZy6yQfn
        usr_name = input("Enter username: ")
        pwd = input("Enter password: ")
        user = Auth().Authenticate(usr_name, pwd)
        
    if not user: # if user is still None, then the user failed all 3 attempts
        PrintFormat("Invalid",'\nFailed all 3 attempts, sorry')
        return
    # user has successfully logged in
    return user

def modifyCarMenu(car):
    PrintFormat("Success", car)
    options = ["1. Change car status",
               "2. Change car price",
               "3. Change car mileage",
               "4. Change car warranty plans"]
    formattedOptions ="\n".join(options)
    PrintFormat('Action', formattedOptions)
    action = getAction(validSet={"1","2","3","4"})

    if not action: return
    elif action == "1": 
        updateCarStatus(car)
    elif action == "2":
        newPrice = ValidateUserInput("new price", True)
        if not newPrice: return
        car.UpdatePrice(newPrice)
    elif action == "3":
        newMileage = ValidateUserInput("new mileage", True)
        if not newMileage: return
        car.UpdateMileage(newMileage)
    else:
        newWarranty = ValidateUserInput("new warranty plans")
        if not newWarranty: return
        car.UpdateWarranty(newWarranty)

def SearchCarMenu(car=None):
    if not car:
        car = CarSearch()
    if car is None: return
    searchOptions = ["1. Order car",
                     "2. Modify car (status, price, mileage, warranty plans)"]

    formattedOptions ="\n".join(searchOptions)
    validate = {"1","2"}
    PrintFormat("Action",formattedOptions)
    action = getAction(validSet=validate)
    if not action: return
    if action == "1": 
        if car.getStatusStr().lower() == "ordered":
            PrintFormat("Invalid", "Car is already ordered")
            return
        addOrderMenu(car, interface.getCustomerList())
    else:
        modifyCarMenu(car)
    
def InventoryMenu():
    PrintFormat("Purple", 'Inventory Menu')
    options = ["0. View car details",
               "1. Search",
               "2. Filter by", 
               "3. Make a customer order"]
    if isAdmin: 
        options.append("4. Add/Remove Cars")

    formattedOptions ="\n".join(options)

    while True:
        inventory = interface.GetInventory()
        displayData(inventory)
        PrintFormat("Action", formattedOptions)
        validateSet = {"0", "1", "2", "3", "4"}
        action = getAction(validateSet)
        if not action: break
        if action == '0':
            carToView = GetObject(inventory)
            print(f"\n{carToView.getDetails()}")
            confirmMsg = f"\nDo you want to modify its details (price, warranty plans, mileage, or status)?"
            if ConfirmSelection(msg=confirmMsg): modifyCarMenu(carToView)
        elif action == '1': SearchCarMenu()
        elif action == '2': filterByMenu()
        elif action == '3': 
            carToOrder = GetObject(inventory)
            if not carToOrder: continue
            addOrderMenu(carToOrder, interface.getCustomerList())
        elif action == '4': modifyInventoryMenu()
            
        StallUntilUserInput()

def AddCar():
    """ Will get user input for a new car and add it to the inventory"""
    vin = input("Enter new car's VIN: ")
    make_model_year = None
    while True:
        make_model_year = SeparateInputToList(input("Enter make, model, year (Separated by commas): "))
        if len(make_model_year) != 3:
            PrintFormat("Invalid", "Make, Model, Year must be separated by a comma")
            continue
        if not make_model_year[2].isnumeric():
            PrintFormat("Invalid", "Year has to be a number")
            continue
        break
    mileage_color = None
    while True:
        mileage_color = SeparateInputToList(input("Enter mileage, color (Separated by commas): "))
        if len(mileage_color) != 2:
            PrintFormat("Invalid", "Mileage and Color must be separated by a comma")
            continue
        if not mileage_color[0].isnumeric():
            PrintFormat("Invalid", "Mileage has to be a number")
            continue
        if not mileage_color[1].isalpha():
            PrintFormat("Invalid", "Color has to be a string")
            continue
        break
    price = input("Enter price: ")
    while not price.isnumeric():
        price = input("HAS TO BE NUMERIC! Enter price: ")
    price = int(price)
    engine_transmission = None
    while True:
        engine_transmission = SeparateInputToList(input("Enter engine, transmission (Separated by commas): "))
        if len(engine_transmission) != 2:
            PrintFormat("Invalid", "Engine and Transmission must be separated by a comma")
            continue
        break
    interior_external_design =None
    while True:
        interior_external_design = SeparateInputToList(input("Enter interior, external design (Separated by commas): "))
        if len(interior_external_design) != 2:
            PrintFormat("Invalid", "Interior and External Design must be separated by a comma")
            continue
        break
    paint = ValidateUserInput("paint")
    handling = [input("Enter handling: ")]
    audio = [input("Enter audio: ")]
    comfort = [input("Enter comfort features: ")]
    package = input("Enter package: ")
    warranty_maintenance = None
    while True:
        warranty_maintenance = SeparateInputToList(input("Enter warranty, maintenance (Separated by commas): "))
        if len(warranty_maintenance) != 2:
            PrintFormat("Invalid", "Warranty and Maintenance must be separated by a comma")
            continue
        break

    info = {"model": make_model_year[1],
            "make": make_model_year[0],
            "mileage": int(mileage_color[0]),
            "year": int(make_model_year[-1]),
            "color": mileage_color[-1],}
    
    performance = {"engine": engine_transmission[0],
                    "transmission": engine_transmission[-1]}
    
    design = {"interior": [interior_external_design[0]],
              "exterior": [{"paint": paint,"extra": [interior_external_design[-1]]}]}
    
    protection = {"maintenance": warranty_maintenance[1], "warranty": [warranty_maintenance[0]]}
    status = getAction(validSet={"ordered", "available", "backorder", "delivered"}, msg="Enter status: ")
    if not status: return
    add = interface.AddInventory(vin, info=info, performance=performance,comfort=comfort, design=design, protection=protection, price=price, handling=handling, package=package, entertainment=audio, status=status)    
    if add:
        PrintFormat("Success", "Car successfully added")
    else:
        PrintFormat("Invalid", "Car already exists")

def RemoveCar():
    if not interface.GetInventory():
        PrintFormat("Invalid", "No cars in inventory")
        return
    car_to_delete = GetObject(interface.GetInventory())
    confirm_msg = f"Are you sure you want to delete {car_to_delete}"

    if interface.isCarOrdered(car_to_delete):
        confirm_msg += f" {bcolors.BOLD}it has been ordered{bcolors.ENDC}"
    if not ConfirmSelection(msg=confirm_msg): return
    rem = interface.RemoveInventory(car_to_delete)
    if rem:
        PrintFormat("Success", "Removed car successfully")
    else:
        PrintFormat("Invalid", "Car not found")

def addOrderMenu(carToOrder, customers):
    PrintFormat('Important', f"\nYou are about to order this car: {carToOrder}")
    if not ConfirmSelection(): return
    # check new customer
    customer = None
    confirmMessage = "Is this order for a new customer?"
    if ConfirmSelection(msg=confirmMessage):
        customer = AddCustomer()
    else: # get from old customers 
        if isEmpty(customers): return
        customer = GetObject(customers)

    if not customer: return
    order = interface.MakeOrder(customer, carToOrder, seller=user)
    if not order:
        PrintFormat("Invalid", "Failed to make order. This car has already been ordered by someone else.")
        return
    PrintFormat("Success", order)

def OrderMenu():
    PrintFormat('Purple','Order Menu')
    options = ["What would you like to do?",
               "1. Add order",
               "2. Remove order",
               "3. View order details"]
    formattedOptions ="\n".join(options)
    while True:
        orders = interface.viewOrders()
        inventory = interface.GetInventory()
        customers = interface.getCustomerList()
        displayData(orders)
        PrintFormat("Action", formattedOptions)
        action = getAction() # get user option choice
        if not action: break
        if action == "1":
            if isEmpty(inventory): continue
            carToOrder = GetObject(inventory)
            if not carToOrder: break
            addOrderMenu(carToOrder, customers)
        else:
            # checker for empty orders
            if isEmpty(orders): continue
            if action == "2":
                orderToRemove = GetObject(orders)
                confirmMessage = f"Are you sure you want to remove this order: {orderToRemove}?"
                if not ConfirmSelection(msg=confirmMessage): break
                if not orderToRemove: break
                interface.UndoOrder(orderToRemove)
            else:
                orderToView = GetObject(orders)
                if not orderToView: break
                print(orderToView.orderDetails())
                # change status
                confirmMessage = "Would you like to change the order status?"
                if ConfirmSelection(msg=confirmMessage): updateCarStatus(orderToView.getCar())

        StallUntilUserInput()

def ManageEmployeesMenu():
    PrintFormat("Purple","Employee Management Menu")
    # if not admin, return as they do not have permissions to view this menu
    if not isAdmin: return
    options = ["1. View Employee details", 
               "2. Add Employee", 
               "3. Remove Employee"]
    formattedOptions ="\n".join(options)
    while True:
        employees = interface.getEmployeeList()
        displayData(employees)
        PrintFormat("Action",f"{formattedOptions}")
        action = getAction()
        if not action: break

        if action == "2": AddEmployee()
        else:
            if isEmpty(employees):  continue
            if action == "1":
                employee = GetObject(employees)
                if not employee: break
                print(employee.getDetails()) # print info like when employee joined
            else:
                RemoveEmployee()

        StallUntilUserInput() # to get user time to read message before going back to next iteration of menu

def validateCreditCard():
    creditCard = input('Credit Card #: ')
    while len(creditCard) != 16:
        PrintFormat("Invalid", "Credit card # needs 16 digits and needs to be digits only")
        creditCard = input('Credit Card #: ')
        if not creditCard.isdigit(): continue
    return creditCard

def modifyCustomerDetails(customer=None):
    if not customer:
        customer = GetObject(interface.getCustomerList())
        if not customer: return
    options = ["1. Update home address",
               "2. Update email address",
               "3. Update card details"]
    formattedOptions = "\n".join(options)
    PrintFormat("Action", f"{formattedOptions}")
    action = getAction()
    if not action: return
    elif action == "1":
        address = ValidateUserInput("new address")
        if not address: return
        interface.changeCustomerAddress(customer, address)
    elif action == "2":
        email = ValidateUserInput("new email", isEmail=True)
        if interface.emailExists(email):
            PrintFormat("Invalid", "Email already exists")
            return
        interface.changeCustomerEmail(customer, email)
    else:
        cardNum = validateCreditCard()
        if not cardNum: return
        interface.changeCustomerCard(customer, cardNum)

def ManageCustomersMenu():
    options = ["1. View Customer details",
               "2. Add Customer", 
               "3. Remove Customer", 
               "4. Edit Customer details"]
    formattedOptions = "\n".join(options)
    while True:
        customers = interface.getCustomerList()
        PrintFormat("Purple","Customer list")
        displayData(customers)
        PrintFormat("Action",f"{formattedOptions}")
        # validate input
        validSet = {"1","2","3","4"}
        action = getAction(validSet=validSet)
        if not action: break
        if action == "2":
            AddCustomer()
        else:
            if isEmpty(customers): continue
            customer = GetObject(customers)
            if not customer: continue

            if action == "1": 
                print(customer.getDetails())
                # update details
                confirmMessage = "Would you like to update customer details?"
                if ConfirmSelection(msg=confirmMessage): modifyCustomerDetails(customer)
            elif action == "3":
                DeleteCustomer(customer)
            else:
                modifyCustomerDetails(customer)

        StallUntilUserInput()

def CarSalesMenu():
    #TODO: Assigned to Dariya
    # display orders
    # Set order statuses to delivered 
    pass

def AccountSettingsMenu():
    """ This is the menu users interact with when they want to change their account details such as password or username """
    PrintFormat("Purple","Account settings")
    options = ["1. Change password",
               "2. Change username", 
               "3. View Account Details"]
    formattedOptions ="\n".join(options)
    while True:
        PrintFormat("Action",f"{formattedOptions}")
        action = getAction()
        if not action: break

        if action == "1":
            ChangePasswordMenu()
        elif action == "2":
            ChangeUsernameMenu()
        else:
            print(f"\nUser {user.getUsername()} details:\n{user}")

        StallUntilUserInput()

def menu():
    """ Main menu that the users will first interact with. Calls on otther menus """
    # made these global because almost all menus need it
    # the options are stored as list, so its easier to add/remove options
    options = ["1. Customer Orders",
               "2. Car Sales",
               "3. Car Inventory",
               "4. Manage Customers"]
    # creating the interface based on the user type
    # employees, get the regular interface, whereas admins get the admin interface which gives them more options
    if isAdmin:
        options.append("5. Manage Employees")

    options.append("A: Account settings") # to allow users to change their passwords/username
    formattedOptions = "\n".join(options) # this is what will be displayed to the users from the options list

    while True: # menu start
        PrintFormat("Success", f"\nHi {user.getFirstName()}, what would you like to do?")
        PrintFormat('Action',formattedOptions) # display options to user
        # validating user choice
        action = getAction({"1", "2", "3", "4", "5", "a"})
        if not action: break # if user presses q, break out of the loop and return to main menu
        # calls menu based on user choice
        {"1": OrderMenu,
         "2": CarSalesMenu,
         "3": InventoryMenu,
         "4": ManageCustomersMenu,
         "5": ManageEmployeesMenu,
         "a": AccountSettingsMenu}[action]()
    
    # TODO: Log off and write to files, awaiting Kate's update
    # interface.LogOut()

def run():
    global user 
    global interface
    global isAdmin

    while True:
        user = Login()
        if not user:
            break

        isAdmin = (user.getCategory().lower() == "admin")
        if not isAdmin: 
            interface = Interface()
        else: 
            interface = AdminInterface()
        menu()
        interface.LogOut()
        if ConfirmSelection(msg="Would you like to log in again?"): continue
        break
        

if __name__ == "__main__":
    run()
