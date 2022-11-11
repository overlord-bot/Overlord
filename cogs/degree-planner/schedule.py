from array import *

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .rules import Rule


#########################################################################
#                              SCHEDULE:                                #
#                                                                       #
# This class is created for each schedule. A user should be able to     #
# create multiple schedules. A schedule may contain user specific data  #
#########################################################################

# TODO: add export function that transfers course lists between schedules
# without transferring any user specific data


class Schedule():
    # SCHEDULE GLOBAL VARIABLES

    def __init__(self, name:str):
        # needs to be initialized before every use by calling master_list_init()
        # uses 2D array [semester][course]
        self.__master_list = []
        self.SEMESTERS_MAX = 12
        self.name = name
        self.degree = None
        self.master_list_init()

    #-----------------------------------------------------------------------
    # Initializes the data structure storing all courses in the schedule,
    # grouped by semester
    #-----------------------------------------------------------------------

    def master_list_init(self):
        self.__master_list.clear()

        # Generates 12 empty lists within master_list. Each list represents a semester
        # with element 0 representing semester 1 and so on.
        for x in range(0, 12):
            self.__master_list.append([])

    #-----------------------------------------------------------------------
    # Main scheduling functions
    #-----------------------------------------------------------------------

    def add_course(self, course, semester) -> bool:
        if semester in self.find_course(course):
            return False
        else:
            self.__master_list[semester].append(course)
            return True


    def remove_course(self, course, semester) -> bool:
        if semester not in self.find_course(course):
            return False
        else:
            self.__master_list[semester].remove(course)
            return True


    def get_semester(self, semester:int) -> list:
        if semester not in range(0, self.SEMESTERS_MAX):
            return None
        else:
            return self.__master_list[semester]

    def get_all_courses(self) -> set:
        courses = set()
        for a in self.__master_list:
            for c in a:
                courses.add(c)
        return courses

    # Returns list of semesters that the course is present in
    def find_course(self, course:Course) -> list:
        i = 0
        present_in = []
        for courselist in self.__master_list:
            if course in courselist:
                present_in.append(i)
            i+=1
        return present_in

    def __len__(self):
        i = 0
        for sem in self.__master_list:
            i += len(sem)
        return i

    def __eq__(self, other):
        if not isinstance(other, Schedule):
            return False
        return self.__master_list == other.__master_list

    def __repr__(self):
        count = 0
        s = f"Schedule: {self.name} [{self.degree.name if self.degree != None else ''}]\n"
        for courselist in self.__master_list:
            s+=f"  Semester {str(count)}:\n"
            count+=1
            for course in courselist:
                s+=f"    Course info: {course.display_name} {course.major} {str(course.course_id)}\n"
        return s

    def __hash__(self):
        i = hash(self.degree)
        sem = 0
        for sem in self.__master_list:
            for course in sem:
                i += hash(course) * sem
            sem += 1
        return i