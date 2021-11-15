from zmq.sugar.constants import NULL
import Job_type as jt
import Abilities as ab
import json

class Employee:
    codeEM = 0
    JO_categories = ""
    age = 0
    connect = True
    capacities = ab.Abilities(0)

    def __init__(self, name, password, funct):
        self.name=name
        self.password=password
        self.funct = funct
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
        return f'{self.funct} {self.codeEM} {self.name} {self.password} {self.age} {self.connect} {self.capacities} {str(self.JO_categories)}'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

"""
emplo1 = Employee("carlos","222", "hola")
print(emplo1)
print(emplo1.__str__)
"""

#print(json.dumps(emplo1, default=lambda o: o.__dict__))
#print(json.loads(json.dumps(emplo1, default=lambda o: o.__dict__)))
