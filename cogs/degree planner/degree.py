from array import *

class Degree():

    name = "" # name of the degree program
    list_and_rules = [] # list of List_and_rules objects that dictate requirements for this degree

    def to_string(self):
        return self.name

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def __hash__(self):
        return hash(self.name)