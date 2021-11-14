from Enum import Academic_formation as af

class Abilities:
    capacitiesList = []

    def __init__(self):
        self.years = int(input("Ingrese los años de experiencia: "))
        cent = True
        while(cent):
            opc = input("Desea añadir una capacidad (S/N): ")
            if(opc == "S"):
                self.addCapacity(input("Ingrese la capacidad: "))
            else:
                cent = False
        self.typeAF = af.Academic_formation(
            int(input("Seleccione el tipo de formacion:\nPROFESIONAL = 1\nPOSGRADO = 2\nMAESTRIA = 3\nDOCTORADO = 4\n"))).name

    def addCapacity(self, string):
        self.capacitiesList.append(string)

    def __str__(self):
        return f'Años de experiencia: {self.years}, Capacidades: {self.capacitiesList}, Tipo de formación: {self.typeAF}'