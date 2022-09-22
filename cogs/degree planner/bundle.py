from array import *
from .course import Course

class Bundle(Course):
# A bundle represents a list of classes, inherits from course so this can be plugged in freely in place of a course

    course_bundle = []

    def add_to_bundle(course):
        self.course_bundle.append(course)

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

    def __hash__(self):
        i = 0
        for course in self.course_bundle:
            i+=course.id
        return i