
class User:

    funct = ""
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __str__(self):
        return f'{self.funct} {self.username} {self.password}'