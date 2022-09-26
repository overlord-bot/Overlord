from array import *
from discord.ext import commands
import discord
import asyncio

from .course import Course
from .degree import Degree

class Catalog():

    # catalog will  be a list of courses and degrees
    # TODO also store graphs for further analysis and course prediction of free electives

    course_list = dict() # course name as key
    degree_list = dict() # degree name as key


    def add_course(self, course):
        self.course_list.update({course.name:course})


    def add_degree(self, degree):
        self.degree_list.update({degree.name:degree})


    def to_string(self):
        count1 = 1
        printout = ""
        for course in self.course_list.values():
            printout+=str(count1) + ": " + course.to_string() + "\n"
            count1+=1
        count1 = 1
        for degree in self.degree_list.values():
            printout+=str(count1) + ": " + degree.to_string() + "\n"
            count1+=1
        return printout