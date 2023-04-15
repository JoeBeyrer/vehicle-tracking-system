from parsers import *
from PigeonBox import session, status, orders, users, vehicles

class InterfaceObjects():
    def __init__(self) -> None:
        self.inventory = readJson.LoadInventory()
        self.customers = readJson.LoadCustomers()
        self.employees = session.Session().ReturnEmployees()
        self.admins = session.Session().ReturnAdmins()
        self.__users__ = self.employees + self.admins # helper

    # mapper functions
    def usernameToUser(self, username):
        for user in self.__users__:
            if user.getUsername() == username:
                return user
    
    def vinToCar(self, vin):
        for car in self.inventory:
            if car.getVin() == vin:
                return car
    
    def emailToCustomer(self, emailAddress):
        for customer in self.customers:
            if customer.getEmail() == emailAddress:
                return customer
            
    def getCustomerList(self):
        return self.customers
    
    def getEmployeeList(self):
        return self.employees

    def isEmployee(self, user):
        return user in self.employees

    def ViewUsers(self):
        return self.__users__
    
    def vinExists(self, vin):
        for car in self.inventory:
            if car.getVin() == vin:
                return True
        return False
        
    def inInventory(self, car):
        if isinstance(car, str):
            return self.vinExists(car)

        for vehicle in self.inventory:
            if vehicle == car:
                return True
        return False 
    
    def ViewByStatus(self, statusToViewBy):
        statusToViewBy = statusToViewBy.lower()

        if (statusToViewBy == 'available'):
            return self.ViewAvailableInventory()

        viewStatus = status.strToStatus(statusToViewBy)
        filteredByStatus = []
        for car in self.inventory:
            if car.getStatus() == viewStatus:
                filteredByStatus.append(car)

        return filteredByStatus
    
    def GetInventory(self):
        return self.inventory
    
    def searchInventory(self, model, make, year):
        """ Given relevant info, finds and returns a car object"""
        for car in self.inventory:
            info = car.getCarInfo()
            if model == info['model'] and make == info['make'] and year == info['year']:
                return car
    
    def ViewAvailableInventory(self):
        available = []
        for vehicle in self.inventory:
            if vehicle.getStatus() == status.Status.AVAILABLE:
                available.append(vehicle)
        return available
    
    def UserExists(self, checkUser):
        """ Useful for when we want to add or remove an employee"""
        if (isinstance(checkUser, str)):
            return self.UsernameExists(checkUser)
        
        for user in self.__users__:
            if user == checkUser:
                return True
        return False
    
    # def customerExists
    
    def UsernameExists(self, username):
        for user in self.__users__:
            if user.getUsername() == username:
                return True
        return False

class Interface(InterfaceObjects):
    def __init__(self) -> None:
        super().__init__()
        self.ordersDict = readJson.LoadOrders() # have to pass customers and car functionality to correctly add to buyers list and such
        self.orders = []
        for order in self.ordersDict:
            self.orders.append(orders.Order(id=order['id'], 
                                            car=self.vinToCar(order['carVin']), 
                                            buyer=self.emailToCustomer(order['buyer']), 
                                            employee=self.usernameToUser(order['soldBy']), 
                                            dateBought=order['dateBought']))

        # 0: inv, 1: order, 2: users, 3: customer
        self.isObjListUpdated = [False] * 4

        # loading customer orders if there's any
        for order in self.orders:
            currentCustomer = order.getUser()
            for customer in self.customers:
                if customer == currentCustomer:
                    customer.orders.append(order)

    def changeCarStatus(self, car, status):
        car.SetStatus(status)
        self.isObjListUpdated[0] = True

    def changeCarPrice(self, car, newPrice):
        car.UpdatePrice(newPrice)
        self.isObjListUpdated[0] = True
    
    def changeCarMileage(self, car, newMileage):
        car.UpdateMileage(newMileage)
        self.isObjListUpdated[0] = True

    def changeCustomerEmail(self, customer, newEmail):
        customer.setEmail(newEmail)
        self.isObjListUpdated[3] = True

    def changeCustomerCard(self, customer, newCard):
        customer.setCard(newCard)
        self.isObjListUpdated[3] = True
    
    def changeCustomerAddress(self, customer, newAddress):
        customer.setAddress(newAddress)
        self.isObjListUpdated[3] = True

    def changeUserPassword(self, user, newPassword):
        for admin in self.admins:
            if admin == user:
                admin.UpdatePassword(newPassword)
                self.isObjListUpdated[2] = True
                return
        
        for employee in self.employees:
            if employee == user:
                employee.UpdatePassword(newPassword)
                self.isObjListUpdated[2] = True
                return
            
    def changeUserUsername(self, user, newUsername):
        for admin in self.admins:
            if admin == user:
                admin.UpdateUserName(newUsername)
                self.isObjListUpdated[2] = True
                return
        
        for employee in self.employees:
            if employee == user:
                employee.UpdateUserName(newUsername)
                self.isObjListUpdated[2] = True
                return
            
    def viewOrders(self):
        return self.orders
    
    def getOrderslist(self):
        return self.orders
    
    def isCarOrdered(self, car) -> bool:
        for order in self.orders:
            if order.getCar() == car:
                return True
        return False
    
    def doesOrderExist(self, checkOrder) -> bool:
        for order in self.orders:
            if order == checkOrder:
                return True
        return False
    
    def MakeOrder(self, customer, vehicle, seller):
        # check that a vehicle is available before making an order
        if not vehicle.isAvailable(): return
        id = self.orders[-1].getId() + 1 if self.orders else 1
        order = orders.Order(id, vehicle, customer, employee=seller) # create order object
        # add order to order list and deal with the customer dependency
        self.orders.append(order)
        customer.orders.append(order)
        self.isObjListUpdated[1] = True # to write to json -- orders have been updated
        return order
    
    def UndoOrder(self, order):
        # will remove an order from the orders list and update the car status
        # also removes order from the users.orders list
        if not self.doesOrderExist(order): 
            return
        
        self.orders.remove(order)
        order.RemoveOrder()
        del order # delete order object and free up memory

        self.isObjListUpdated[1] = True

    def emailExists(self, email):
        for customer in self.customers:
            if customer.getEmail() == email:
                return True
        return False

    def isCustomer(self, newCustomer):

        if isinstance(newCustomer, str):
            return self.emailExists(newCustomer)

        for customer in self.customers:
            if customer == newCustomer:
                return True
        return False

    def AddCustomer(self, first, last, card, email, address):
        if self.isCustomer(email):
            return
        newCustomer = users.Customer(first, last, card, email, address)
        self.customers.append(newCustomer)
        self.isObjListUpdated[3] = True
        return newCustomer

    def RemoveCustomer(self, customer):
        """delete from orders if they exist AND set car to available if customer has been deleted """
        # grab customer orders
        customerOrders = []
        for order in self.orders:
            if order.getUser() == customer:
                customerOrders.append(order)
                if order.getCar().getStatus() != status.Status.ORDERED: # if car has not been delivered yet
                    order.getCar().setStatus(status.Status.BACKORDER)
        # delete orders for customers:
        while customerOrders:
            order = customerOrders.pop()
            self.UndoOrder(order)
        # delete customer
        self.customers.remove(customer)
        del customer
        self.isObjListUpdated[3] = True

    def LogOut(self):
        if self.isObjListUpdated[0]:
            writeJson.writeJson(self.inventory)
        if self.isObjListUpdated[1]:
            writeJson.writeJson(self.orders)
        if self.isObjListUpdated[2]:
            allUsers = self.admins + self.employees
            writeJson.writeJson(allUsers)
        if self.isObjListUpdated[3]:
            writeJson.writeJson(self.customers)

class AdminInterface(Interface):
    """ Admin can do everything an employee can do and MORE, hence why it has its own class, which inherits all the methods from Interface
        but an admin can add and remove employees, and add and remove cars from inventory """

    def AddAdmin(self, username, passwd, fname, lname, dateJoined=None):
        if self.UserExists(username):
            return False
        
        newAdmin = users.Admin(username, passwd, fname, lname, date_joined=dateJoined)
        self.admins.append(newAdmin)
        self.isObjListUpdated[2] = True
        return True

    def AddEmployee(self, username, passwd, fname, lname, dateJoined=None) -> None:
        if self.UserExists(username):
            return False
        
        newEmployee = users.Employee(username, passwd, fname, lname, date_joined=dateJoined)
        self.employees.append(newEmployee)
        self.isObjListUpdated[2] = True
        return True
    
    def ordersMadeByUser(self, user):
        orders = []
        for order in self.orders:
            if order.getSeller() == user:
                orders.append(order)
        return orders

    def RemoveUser(self, userToRemove) -> bool:
        if not self.UserExists(userToRemove):
            return False

        # remove all orders made by that user
        userOrders = self.ordersMadeByUser(userToRemove)
        if userOrders:
            for order in userOrders:
                self.UndoOrder(order)

        if (isinstance(userToRemove, users.Admin)):
            self.admins.remove(userToRemove)
        else:
            self.employees.remove(userToRemove)

        self.__users__.remove(userToRemove)
        self.isObjListUpdated[2] = True
        return True

    def AddInventory(self, vin, info, performance, design, handling, comfort, entertainment, protection, package, price, status=None) -> bool:
        """ checks if car already exist, if it doesn't, adds it to the inventory"""
        if self.inInventory(vin): 
            return False 
        
        newCar = vehicles.Car(vin=vin, info=info, performance=performance, design=design, handling=handling, comfort=comfort, entertainment=entertainment, protection=protection, package=package, price=price, status=status)
        self.inventory.append(newCar) 
        self.isObjListUpdated[0] = True 
        return True 

    def RemoveInventory(self, car) -> bool:
        """ checks if car exists, if it does, checks the status of the car, if it is ordered then it also removes the order
        then proceeds by removing the car entirely from the system"""
        if not self.inInventory(car): return False
        if car.getStatus() == status.Status.ORDERED:
            currentOrder = None
            for order in self.orders:
                if order.getCar() == car: 
                    currentOrder = order 
                    break
            if currentOrder: self.UndoOrder(currentOrder)
        self.inventory.remove(car)
        self.isObjListUpdated[0] = True
        return True
