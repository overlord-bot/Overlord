from array import *
from discord.ext import commands
import discord
import asyncio

from .course import Course
from .catalog import Catalog
from .degree import Degree
from .bundle import Bundle
from .list_and_rules import List_and_rules


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

    def __init__(self):
        # needs to be initialized before every use by calling master_list_init()
        # uses 2D array [semester][course]
        self.master_list = []

    #-----------------------------------------------------------------------
    # Initializes the data structure storing all courses in the schedule,
    # grouped by semester
    #-----------------------------------------------------------------------

    def master_list_init(self):
        print("initializing master_list")
        self.master_list.clear()

        # Generates 12 empty lists within master_list. Each list represents a semester
        # with element 0 representing semester 1 and so on.
        for x in range(0, 12):
            self.master_list.append([])
        print("initializing master_list complete")

    #-----------------------------------------------------------------------
    # Main scheduling functions
    #-----------------------------------------------------------------------

    def add_course(self, course, semester):
        if semester in self.find_course(course):
            print("cannot add course as it's duplicated")
        else:
            self.master_list[semester].append(course)


    def remove_course(self, course, semester):
        if semester not in self.find_course(course):
            print("course not present in semester" + str(semester))
        else:
            self.master_list[semester].remove(course)


    # Parameters: course to find
    # Returns: semesters that the course is present in
    def find_course(self, course):
        i = 0;
        present_in = []
        for courselist in self.master_list:
            if course in courselist:
                present_in.append(i)
            i+=1
        return present_in


    # prints student's schedule to a string
    def to_string(self):
        count = 0
        s = ""
        for courselist in self.master_list:
            count+=1
            s+="Semester " + str(count) + ":\n"
            for course in courselist:
                s+="\tCourse info: " + course.name + " " + course.major + " " + str(course.course_id) + "\n"
        return s