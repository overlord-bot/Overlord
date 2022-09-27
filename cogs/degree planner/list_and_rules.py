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

    def longest(self, coursedict):
        i = 0
        for path in coursedict:
            if len(path) > i:
                i = len(path)
        return i

    def fulfilled(self):
        courses = 0
        courses_2k = 0
        courses_4k = 0
        courses_CI = 0
        required_copy = self.required_courses
        same_concentration = dict()
        same_pathway = dict()

        for course in self.course_list:
            courses+=1
            if course.level() == 2:
                courses_2k+=1
            if course.level() == 4:
                courses_4k+=1
            if course.CI:
                courses_CI+=1
            if course in required_copy:
                required_copy.remove(course)
            if course.HASS_pathway in same_pathway:
                same_pathway.get(course.HASS_pathway).append(course)
            elif course.HASS_pathway != "":
                same_pathway.update(course.HASS_pathway, [course])
            if course.concentration in same_concentration:
                same_concentration.get(course.concentration).append(course)
            elif course.concentration != "":
                same_concentration.update(course.concentration, [course])

        if (courses < self.min_courses or courses_2k < self.min_2000_courses or courses_4k < self.min_4000_courses 
            or courses_CI < self.min_CI or required_copy or self.longest(same_concentration) < self.min_same_concentration
            or self.longest(same_pathway) < self.min_same_pathway):
            return False
        return True