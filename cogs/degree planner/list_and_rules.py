from array import *
from .course import Course


# A list of classes and the rules that determines requirement fulfillment statuses.


class List_and_rules():

    course_list = []
    min_courses = 0
    min_2000_courses = 0
    min_4000_courses = 0
    min_CI = 0
    required_courses = []
    min_same_concentration = 0
    min_same_pathway = 0

    def fulfilled(self):
        courses = 0
        courses_2k = 0
        courses_4k = 0
        courses_CI = 0
        required_copy = self.required_courses
        #same_concentration = dict()
        #same_pathway = dict()

        for course in self.course_list:
            courses+=1
            if course.level() == 2:
                courses_2k+=1
            if course.level() == 4:
                courses_4k+=1
            if course.CI:
                courses_CI+=1
            #TODO add pathway and concentration counter here
            if course in required_copy:
                required_copy.remove(course)

        if courses < self.min_courses or courses_2k < self.min_2000_courses or courses_4k < self.min_4000_courses or courses_CI < self.min_CI or required_copy:
            return False
        return True