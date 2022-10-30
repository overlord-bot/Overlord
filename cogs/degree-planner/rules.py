from array import *
from .course import Course

# A list of classes and the rules that determines requirement fulfillment statuses.

class Rules():

    label = ''

    course_list = []
    min_courses = 0
    min_2000_courses = 0
    min_4000_courses = 0
    min_CI = 0
    required_courses = []
    min_same_concentration = 0
    min_same_pathway = 0

    # finds the longest list within a list of lists
    def longest(self, main_list):
        i = 0
        longest_path = []
        for path in main_list.values():
            if i < len(path):
                i = len(path)
                longest_path = path
                
        return longest_path

    def longest_name(self, main_list):
        i = 0
        longest_path_name = ""
        for path_name in main_list.keys():
            if i < len(main_list[path_name]):
                i = len(main_list[path_name])
                longest_path_name = path_name
                
        return longest_path_name

    def fulfillment(self):
        courses = 0
        courses_2k = 0
        courses_4k = 0
        courses_CI = 0
        required_copy = self.required_courses
        same_concentration = dict()
        same_pathway = dict()

        status_return = ""

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

            for pathway in course.HASS_pathway:
                if pathway in same_pathway:
                    list_returned = same_pathway.get(pathway)
                    list_returned.append(course)
                    same_pathway.update({pathway:list_returned})
                else:
                    same_pathway.update({pathway:[course]})

            for concentration in course.concentration:
                if concentration in same_concentration:
                    list_returned = same_concentration.get(concentration)
                    list_returned.append(course)
                    same_concentration.update({concentration:list_returned})
                else:
                    same_concentration.update({concentration:[course]})

        # course fulfillment
        if (courses < self.min_courses):
            status_return += f"Minimum course number not met: {courses} of minimum {self.min_courses} taken for rule {self.label}\n"

        if (courses_2k < self.min_2000_courses):
            status_return += f"Minimum course number not met: {courses_2k} of minimum {self.min_2000_courses} 2000 level courses taken for rule {self.label}\n"

        if (courses_4k < self.min_4000_courses):
            status_return += f"Minimum course number not met: {courses_4k} of minimum {self.min_4000_courses} 4000 level courses taken for rule {self.label}\n"

        if (courses_CI < self.min_CI):
            status_return += f"Minimum CI courses not met: {courses_CI} of minimum {self.min_CI} communication intensive courses taken for rule {self.label}\n"

        for c in required_copy:
            status_return += f"Required course {c} not taken for rule {self.label}\n"

        if (len(self.longest(same_concentration)) < self.min_same_concentration):
            status_return += f"Need {self.min_same_concentration} courses in the same concentration for rule {self.label}"
            status_return += f"current longest concentration you have taken is {self.longest_name(same_concentration)}"

        if (courses < self.min_courses or courses_2k < self.min_2000_courses or courses_4k < self.min_4000_courses 
            or courses_CI < self.min_CI or required_copy or len(self.longest(same_concentration)) < self.min_same_concentration
            or len(self.longest(same_pathway)) < self.min_same_pathway):
            return False
        return status_return

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

            for pathway in course.HASS_pathway:
                if pathway in same_pathway:
                    list_returned = same_pathway.get(pathway)
                    list_returned.append(course)
                    same_pathway.update({pathway:list_returned})
                else:
                    same_pathway.update({pathway:[course]})

            for concentration in course.concentration:
                if concentration in same_concentration:
                    list_returned = same_concentration.get(concentration)
                    list_returned.append(course)
                    same_concentration.update({concentration:list_returned})
                else:
                    same_concentration.update({concentration:[course]})


        if (courses < self.min_courses or courses_2k < self.min_2000_courses or courses_4k < self.min_4000_courses 
            or courses_CI < self.min_CI or required_copy or len(self.longest(same_concentration)) < self.min_same_concentration
            or len(self.longest(same_pathway)) < self.min_same_pathway):
            return False
        return True