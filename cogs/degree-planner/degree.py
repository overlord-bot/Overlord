from array import *
import json

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

    def add_rule(self, rule):
        self.rules.add(rule)

    def fulfillment(self, taken_courses:set):
        status_return = dict()
        for rule in self.rules:
            status_return.update(rule.fulfillment(taken_courses))
        return status_return

    def fulfillment_msg(self, taken_courses:set):
        status_return = ""
        for rule in self.rules:
            status_return = f"Rule {rule.name}: \n{rule.fulfillment_return_message(taken_courses)}\n"
        return status_return

    def json(self):
        degree = dict()
        rules = list()
        for r in self.rules:
            rules.append(r)
        degree.update({self.name:r})
        return json.dumps(degree)


    def __repr__(self):
        return f"{self.name}: {str(self.rules)}"

    def __eq__(self, other):
        if not isinstance(other, Degree):
            return False
        if self.name == other.name and self.rules == other.rules:
            return True
        return False

    def __hash__(self):
        i = 0
        for r in self.rules:
            i += hash(r)
        i += hash(self.name)
        return i