
from array import *
from .bundle import Bundle

class Major(Bundle):

    name = ""
    core_course = [] # list of pair,mall the core course that the major required to graduate, ("MATH",MATH bundle core)
    ris_course = [] # list of pair, with number of courses need to take in the list, and bundle of restricted course in the category
                    # (1,bundle) means need to take one out of three course, NOT SURE ABOUT THIS YET
    def __init__(self, major_name):
        self.name = major_name

    def add_core(self,course):
        i = len(self.core_course)
        while(i > 0): # find the element in the list with the course major or loop to end
            if(self.core_course[i].get_title == course.major):
                break
            --i

        if(i == 0 ): # no such course bundle yet
            self.core_course.append(Bundle(course,course,course.major))
            self.core_course[-1].add(course)
        else: # find the element of the major courses
            self.core_course[i].add(course)


    def remove_core(self, course):
        i = len(self.core_course)
        while(i > 0): # find the element in the list with the course major or loop to end
            if(self.core_course[i].get_title == course.major):
                break
            --i

        if(i != 0):
            self.core_course[i].remove(course)

    def add_ris(self,bundle_index, course):
        self.ris_course[bundle_index][2].add(course)

    def remove_ris(self, bundle_index, course):
        self.ris_course[bundle_index][2].remove(course)

    #def check_core(self,course_taken): # input a bundle of







