from array import *
from .course import Course

# A bundle represents a list of classes, inherits from course so this can be plugged in freely in place of a course

class Bundle(Course):

    def __init__(self, title, b, c):
        self.__course_bundle = set()
        self.title = title

    def add(self, course) -> None:
        self.__course_bundle.add(course)

    def remove(self, course) -> None:
        self.__course_bundle.remove(course)

    def set_bundle(self, course_set) -> None:
        for c in course_set:
            self.add(c)

    def get_bundle_set(self) -> set:
        return self.__course_bundle

    def contains(self, course:Course) -> bool:
        return course in self.__course_bundle

    def to_string(self) -> str:
        return ",".join(self.__course_bundle)

    def __len__(self) -> int:
        return len(self.__course_bundle)

    def __eq__(self, other) -> bool:
        mylist = self.__course_bundle
        otherlist = other.__course_bundle

        for course in mylist:
            if course not in otherlist:
                return False
            otherlist.remove(course)
        if otherlist:
            return False
        return True

    # see if other is a sublist of self
    def __ge__(self, other) -> bool:
        mylist = self.__course_bundle
        otherlist = other.__course_bundle

        for course in otherlist:
            if course not in mylist:
                return False
        return True

    def __hash__(self) -> int:
        i = 0
        for course in self.__course_bundle:
            i+=course.id
        return i