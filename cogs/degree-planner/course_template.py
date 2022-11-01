from array import *
from .course import Course

class Template():

    def __init__(self, name, template_course):
        self.name = name
        self.template_course = template_course
        self.course_set = set()

    def to_string(self) -> str:
        return ",".join(self.course_set)

    def __len__(self) -> int:
        return len(self.course_set)

    def __eq__(self, other) -> bool:
        mylist = self.course_set
        otherlist = other.course_set

        for course in mylist:
            if course not in otherlist:
                return False
            otherlist.remove(course)
        if otherlist:
            if other.template_course != self.template_course:
                return False
        return True

    # see if other is a sublist of self
    def __ge__(self, other) -> bool:
        mylist = self.__course_bundle
        otherlist = other.__course_bundle

        for course in otherlist:
            if course not in mylist:
                if other.template_course != self.template_course:
                    return False
        return True

    def __hash__(self) -> int:
        i = 0
        for course in self.__course_bundle:
            i+=course.id
        return i