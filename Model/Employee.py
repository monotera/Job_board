
import Abilities as ab
import json

class Employee:
    next_id = 0

    def __init__(self):
        self.name=input("Ingrese su nombre: ")
        self.password=input("Ingrese una contraseña: ")
        self.connect = True
        self.capacities = ab.Abilities()
        self.id = "EM"+ str(Employee.next_id)
        Employee.next_id += 1
    """
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.connect = True
        self.id = "EM"+ str(Employee.next_id)
        Employee.next_id += 1
    """

    def __str__(self):
        return f'ID: {self.id}\nName: {self.name}\nEstado: {self.connect}\nCapacidades: {str(self.capacities)}'

    def addCapacity(self, string):
        self.capacities.append(string)

"""
emplo1 = Employee()
print(str(emplo1))
"""

#print(json.dumps(emplo1, default=lambda o: o.__dict__))
#print(json.loads(json.dumps(emplo1, default=lambda o: o.__dict__)))
