from Enum import Job_type as jt
import Abilities as ab
import json

class Employee:
    next_id = 0
    JO_categories = []

    def __init__(self):
        self.name=input("Ingrese su nombre: ")
        self.password=input("Ingrese una contraseña: ")
        self.age = input("Ingrese su edad: ")
        print("-- Puede seleccionar dos trabajos para seguir --")
        self.JO_categories.append(jt.Job_type(
            int(input("\nSeleccione el primer tipo de trabajo a seguir:\nFUERZAS_MILITARES = 1\nDIRECTORES_GERENTES = 2\nPROFESIONALES_CIENTIFICOS = 3\nTECNICOS_PROFESIONALES = 4\nPERSONAL_APOYO_ADM = 5\nTRABAJADORES_VENDEDORES = 6\n"))).name)
        self.JO_categories.append(jt.Job_type(
            int(input("\nSeleccione el segundo tipo de trabajo a seguir:\nFUERZAS_MILITARES = 1\nDIRECTORES_GERENTES = 2\nPROFESIONALES_CIENTIFICOS = 3\nTECNICOS_PROFESIONALES = 4\nPERSONAL_APOYO_ADM = 5\nTRABAJADORES_VENDEDORES = 6\n"))).name)
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

        self.typeJ = jt.Job_type(
            int(input("\nSeleccione el tipo de trabajo:\nFUERZAS_MILITARES = 1\nDIRECTORES_GERENTES = 2\nPROFESIONALES_CIENTIFICOS = 3\nTECNICOS_PROFESIONALES = 4\nPERSONAL_APOYO_ADM = 5\nTRABAJADORES_VENDEDORES = 6\n"))).name
        

    """

    def __str__(self):
        return f'ID: {self.id}\nName: {self.name}\nEdad: {self.age}\nEstado: {self.connect}\nCapacidades: {str(self.capacities)}\nTtrabajos suscritos: {self.JO_categories}'

    def addCapacity(self, string):
        self.capacities.append(string)

"""
emplo1 = Employee()
print(str(emplo1))
"""

#print(json.dumps(emplo1, default=lambda o: o.__dict__))
#print(json.loads(json.dumps(emplo1, default=lambda o: o.__dict__)))
