from interface import *
from session import Auth

def login_page():
    print('Welcome to PigeonBOX')
    user, attempt = None, 0
    while (user is None and attempt < 3):
        attempt+=1
        usr_name = input("\nEnter username: ")
        pwd = input("Enter password: ")
        user = Auth().authenticate(usr_name, pwd)

    if not user: 
        print('\nFailed all 3 attempts, sorry')
        return
    
    print(f'\nHi {user.first_name} you have successfully logged in')
    return user

def displayCars(data):
    if not data:
        print('No cars match given criteria')
        return

    for i, car in enumerate(data):
        print(f"{i + 1}: {car}")

def inventory_menu(interface, user_in_session):
    print('\nINVENTORY MENU')

    inventory = interface.viewInventory()
    displayCars(inventory)

    options = "\n1. Search\n2. Filter\n3. Sort"
    if isinstance(interface, AdminInterface): options += '\n4. Add inventory\n5. Remove inventory'
    while True:
        print(options)
        decision = input("\nType 'q' to exit inventory menu\nEnter action: ")
        if decision == '1':
            # search
            print('\nSearch car in inventory')
            search_decision = input("Enter model, make and year separated by commas\n")
            search_decision = list(map(lambda x: x.strip(), search_decision.split(',')))
            if len(search_decision) != 3: break
            model, make, year = search_decision[0], search_decision[1], search_decision[2]
            if not year.isnumeric(): 
                print('\nInvalid input')
                break 
            car = interface.searchInventory(model, make, int(year))
            if not car: 
                print('\nNo car match given criteria')
                break
            interface.printCarInfo(car)
            order = input('\nWould you like to order this car? [y/n]\n')
            #TODO
            # finish orders
            if order not in {"yes", "y"}: break
            # ask for user input
            proc = interface.makeOrder(user_in_session, car)
            if not proc:
                print('Order unsuccessful')
                break
            print(proc)

        elif decision == '2':
            print("\nFilter by Status:\n1. Available\n2. Ordered\n3. Backorder\n4. Delivered")
            statuses = {"1": "available", "2": "ordered", "3": "backorder", "4": "delivered"}
            filter_decision = input("\nEnter here: ")
            if filter_decision not in statuses: break
            {"1": displayCars,
             "2": displayCars,
             "3": displayCars,
             "4": displayCars}[filter_decision](interface.viewByStatus(statuses[filter_decision]))
        elif decision == '3':
            if not isinstance(interface, AdminInterface):
                break
        else: return

def order_menu(interface, user):
    print('\nORDER MENU')
    print('\nOrders:\n')
    displayCars(interface.orders)
    while True:
        print('\n1. Add order\n2. Remove order\n3. View order details\nType "q" to go back to main menu')
        action = input("\nEnter action: ")
        if action not in {"1", "2", "3"}: break
        if action == "2":
            # delete
            to_rem = input("\nPick index of order to remove")
            if not to_rem.isnumeric(): 
                print('Invalid option')
                break
            to_rem = int(to_rem) - 1
            #TODO
            if to_rem >= len(interface.orders):
                print('Invalid index')
                break
            # interface.orders[to_rem].remOrder()
            

def employee_menu(interface, user):
    print('in emp')
    pass

def menu():
    user = login_page()
    if not user: return
    
    interface = None
    options = "1. View Inventory\n2. View Orders"
    if isinstance(user, Employee): interface = Interface()
    else: 
        interface = AdminInterface()
        options += '\n3. Add/Remove Employees'
    
    while True:
        print('\nWhat do you wish to do?')
        print(options)
        print('\nType "q" to log off')
        decision = input('Enter choice here: ')
        if not decision in {"1","2","3"}: break
        {"1": inventory_menu,
         "2": order_menu,
         "3": employee_menu}[decision](interface, user)
        
    # interface.logOut()

if __name__ == "__main__":
    menu() # gkubach0 2nBztx3qzXV
    
