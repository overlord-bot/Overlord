from array import *

class Degree():

    def __init__(self, name):
        self.name = name # name of the degree program
        self.rules = set() # set of Rules that dictate requirements for this degree

    def get_core(self):
        pass

    def get_pathways(self):
        pass

    def get_concentrations(self):
        pass

    def get_electives(self):
        pass

    def to_string(self):
        return self.name

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def __hash__(self):
        return hash(self.name)