from array import *
from .course import Course
from .degree import Degree

class Catalog():

    #catalog will  be a list of courses and degrees
    #also store graphs for further analysis and course prediction of free electives

    course_list = dict() # course name as key
    degree_list = dict() # degree name as key

    def add_course(self, course):
        self.course_list.update({self.course.name, course})

    def add_degree(self, degree):
        self.degree_list.update({self.degree.name, degree})