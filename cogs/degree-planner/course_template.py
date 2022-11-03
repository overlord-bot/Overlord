from array import *
from .course import Course

class Template():

    def __init__(self, name, template_course=Course("", "", 0)):
        self.name = name
        self.template_course = template_course
        self.course_set = set()

    def __repr__(self) -> str:
        s = f"Template {self.name}:\n"
        s += f"  {str(self.template_course)}\n"
        s += f"course_set: "
        s += ",".join(self.course_set)
        return s

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

    def __hash__(self) -> int:
        i = hash(self.template_course)**2
        for course in self.course_set:
            i+=hash(course)
        return i