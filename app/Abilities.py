import Academic_formation as af

class Abilities:
    capacitiesList = []
    years = 0
    typeAF = af.Academic_formation(1)


    def __init__(self, years):
        self.years = years

    def addCapacity(self, string):
        self.capacitiesList.append(string)

    def __str__(self):
        return f'{self.years} {self.capacitiesList} {self.typeAF}'