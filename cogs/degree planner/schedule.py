from array import *
from discord.ext import commands
import discord
import asyncio

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .rules import Rules


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
        self.master_list_init()

    #-----------------------------------------------------------------------
    # Initializes the data structure storing all courses in the schedule,
    # grouped by semester
    #-----------------------------------------------------------------------

    def master_list_init(self):
        print("initializing master_list")
        self.__master_list.clear()

        # Generates 12 empty lists within master_list. Each list represents a semester
        # with element 0 representing semester 1 and so on.
        for x in range(0, 12):
            self.__master_list.append([])
        print("initializing master_list complete")

    #-----------------------------------------------------------------------
    # Main scheduling functions
    #-----------------------------------------------------------------------

    def add_course(self, course, semester):
        if semester in self.find_course(course):
            print("cannot add course as it's duplicated")
        else:
            self.__master_list[semester].append(course)
            print(f"added course: {course.to_string()}, semester: {semester}")


    def remove_course(self, course, semester):
        if semester not in self.find_course(course):
            print(f"course not present in semester {str(semester)}")
        else:
            self.__master_list[semester].remove(course)


    def get_semester(self, semester):
        if semester >= len(self.__master_list):
            print("invalid semester")
            return ""
        return self.__master_list[semester]


    # Parameters: course to find
    # Returns: semesters that the course is present in
    def find_course(self, course):
        i = 0;
        present_in = []
        for courselist in self.__master_list:
            if course in courselist:
                present_in.append(i)
            i+=1
        return present_in


    # prints student's schedule to a string
    def to_string(self):
        count = 0
        s = "Schedule: " + self.name + "\n"
        for courselist in self.__master_list:
            s+="  Semester " + str(count) + ":\n"
            count+=1
            for course in courselist:
                s+="    Course info: " + course.name + " " + course.major + " " + str(course.course_id) + "\n"
        return s