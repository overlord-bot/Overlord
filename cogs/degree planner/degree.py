from array import *

class Degree():

    name = ""
    
    list_and_rules = [] #list of List_and_rules objects that dictate requirements for this degree

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def __hash__(self):
        return hash(self.name)