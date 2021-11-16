import Job_type as jt
import Abilities as ab


class JobOffer:
    next_id = 0
    vancacy_queue = []

    def __init__(self):
        self.name = input("Ingrese el nombre del trabajo: ")
        self.vacancies = input("Ingrese el número de vacantes: ")
        self.salary = input("Ingrese el sueldo: ")
        self.typeJ = jt.Job_type(
            int(input("\nSeleccione el tipo de trabajo:\nFUERZAS_MILITARES = 1\nDIRECTORES_GERENTES = 2\nPROFESIONALES_CIENTIFICOS = 3\nTECNICOS_PROFESIONALES = 4\nPERSONAL_APOYO_ADM = 5\nTRABAJADORES_VENDEDORES = 6\n"))).name
        self.capacities = ab.Abilities()
        self.id = "JO" + str(JobOffer.next_id)
        JobOffer.next_id += 1

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
        return f'ID: {self.id}\nNombre: {self.name}\nVacantes: {self.vacancies}\nSalario: {self.salary}\nTipo de trabajo: {self.typeJ}\nCapacidades: {str(self.capacities)}\nVacantes: {self.vancacy_queue}'

    def addCodeEmployee(self, emploID):
        if(int(self.vacancies) > len(self.vancacy_queue)):
            self.vancacy_queue.append(emploID)
        else:
            print("No hay vacantes disponibles")

"""
job1 = JobOffer()
job1.addCodeEmployee("1")
job1.addCodeEmployee("2")
job1.addCodeEmployee("3")

print(str(job1))
"""