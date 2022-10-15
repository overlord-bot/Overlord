from array import *
from .course import Course


# A bundle represents a list of classes, inherits from course so this can be plugged in freely in place of a course


class Bundle(Course):

    course_bundle = []
    title = ""

    def __init__(self, title, b, c):
        self.course_bundle = []
        self.title = title

    def add(self, course):
        self.course_bundle.append(course)

    def remove(self, course):
        self.course_bundle.remove(course)

    def get_title(self):
        return self.title

    def to_string(self):
        string = ""
        for course in self.course_bundle:
            string+=f"[{course.name}] "
        return string

    def __eq__(self, other):
        mylist = self.course_bundle
        otherlist = other.course_bundle

        for course in mylist:
            if course not in otherlist:
                return False
            otherlist.remove(course)
        if otherlist:
            return False
        return True

    def __ge__(self, other): # see if other is a sublist of self
        mylist = self.course_bundle
        otherlist = other.course_bundle

        for course in otherlist:
            if course not in mylist:
                return False
        return True

    def __hash__(self):
        i = 0
        for course in self.course_bundle:
            i+=course.id
        return i