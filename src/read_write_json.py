"""
####################################################################################################################
[replace text and delete in bracket]
PROGRAM [name]:  [purpose of code and function. brief]

PROGRAMMER: Kate Anderson katemakenzie@usf.edu

VERSION 1: written [day] [month] 2023 by [firstInitial]. [lastName]
REVISION [revision# ex: 1.1]: [day] [month] 2023 by [firstInitial]. [lastName] to [purpose of revision]


PURPOSE:
[general purpose of code and each functionality. thorough description]

DATA STRUCTURES:
[major data structures and variables]
[ex: variable LENGTH - integer]

ALGORITHM:
[brief description of logic flow]

ERROR HANDLING:
[brief description error handling]

####################################################################################################################
"""
from vehicles import *
from user import *
import json


def loadInventory():
    cars = []
    with open('data/inventory.json', 'r') as file:
        json_file = json.load(file)
        for car in json_file:
            current_car = Car(vin=car['vin'], info=car['info'][0], performance=car['performance'][0],
                              design=car['design'][0], handling=car['handling'], comfort=car['comfort'],
                              entertainment=car['audio'], protection=car['protection'][0], package=car['package'],
                              price=car['price'])
            cars.append(current_car)
    return cars


def loadUsers():
    customers, admins = [], []
    with open('data/users.json', 'r') as usr_file:
        json_user = json.load(usr_file)
        for i in range(len(json_user)):
            cur = json_user[i]
            name = cur['name'][0]
            # dividing them equally (temporary; for testing)
            user = {0: 'employee', 1: 'admin'}[i % 2]
            if user == 'employee':
                customer = Employee(username=cur['username'], password=cur['password'],
                                    first_name=name['firstName'], last_name=name['lastName'],
                                    date_joined=cur['dateJoined'])
                customers.append(customer)
            else:
                admin = Admin(username=cur['username'], password=cur['password'],
                              first_name=name['firstName'], last_name=name['lastName'],
                              date_joined=cur['dateJoined'])
                admins.append(admin)
    return customers, admins


def loadOrders():
    '''
    Reads the orders from orders.json and formats 
    the objects into an array of type Order. Then,
    it returns the array of type Order
    '''
    orders = []
    with open('data/orders.json', 'r') as ord_file:
        json_order = json.load(ord_file)
        for i in range(len(ord_file)):
            cur = json_order[i]
            current_order = Order(
                car=cur['vin'], user=cur['user'],  dateBought=cur['dateBought'])
            orders.append(current_order)
    return orders

def writeJson(file, data): 
    '''
    This function writes data to a json file (either inventory, orders, or users)
    '''
    with open(file, 'w') as f:
        json.dump(data, f)
