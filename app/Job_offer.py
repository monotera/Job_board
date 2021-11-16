import Job_type as jt
import Abilities as ab
from random import randrange


class JobOffer:
    codeJO = 0
    vancacy_queue = []
    funt = "offer"
    meet = "Viernes-8pm"
    employer = ""

    def __init__(self):
        self.name = "OFF"+str(randrange(1000))+"_"+input("Ingrese el nombre del trabajo: ")
        self.vacancies = input("Ingrese el número de vacantes: ")
        self.salary = input("Ingrese el sueldo: ")
        self.typeJ = jt.Job_type(
            int(input("\nSeleccione el tipo de trabajo:\nFUERZAS_MILITARES = 1\nDIRECTORES_GERENTES = 2\nPROFESIONALES_CIENTIFICOS = 3\nTECNICOS_PROFESIONALES = 4\nPERSONAL_APOYO_ADM = 5\nTRABAJADORES_VENDEDORES = 6\n"))).name
        self.capacities = input("Ingrese la habilidad: ")

    """
    def __init__(self, name, vacancies, salary, typeJ):
        self.name = name
        self.vacancies = vacancies
        self.salary = salary
        self.typeJ = typeJ
        self.id = "JO" + str(JobOffer.next_id)
        JobOffer.next_id += 1
    """
    
    def __str__(self):
        return f'{self.funt} {self.codeJO} {self.name} {self.vacancies} {self.salary} {self.typeJ} {self.capacities} {self.vancacy_queue} {self.meet} {self.employer}'

"""
job1 = JobOffer()
job1.addCodeEmployee("1")
job1.addCodeEmployee("2")
job1.addCodeEmployee("3")

print(str(job1))
"""