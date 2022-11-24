from array import *
from .course import Course

class Template():

    """ This class contains a template course, which contains attributes that
        serves as a filter for courses, and a course set, which is the pool of
        courses we filter from.
    """

    def __init__(self, name, template_course=Course("", "", 0), course_set=set()):
        self.name = name
        self.template_course = template_course
        self.course_set = course_set

    def __repr__(self):
        s = f"Template {self.name}:\n"
        s += f"  {str(self.template_course)}\n"
        s += f"course_set: "
        s += ",".join(self.course_set)
        return s

    def __len__(self):
        return len(self.course_set)

    def __eq__(self, other):
        if not isinstance(other, Template):
            return False
        
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

    def __hash__(self):
        i = hash(self.template_course)**2
        for course in self.course_set:
            i+=hash(course)
        return i