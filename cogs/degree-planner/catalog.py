from array import *
from discord.ext import commands
import discord
import asyncio

from .course import Course
from .degree import Degree
from .bundle import Bundle

class Catalog():

    def __init__(self):
        # catalog will  be a list of courses and degrees
        # TODO also store graphs for further analysis and course prediction of free electives
        self.__course_list = dict() # course name as key
        self.__degree_list = dict() # degree name as key
        self.lock = False


    def add_course(self, course):
        self.__course_list.update({course.name:course})


    def add_degree(self, degree):
        self.__degree_list.update({degree.name:degree})


    def get_course(self, course_name):
        return self.__course_list.get(course_name, "")


    def get_all_courses(self):
        return self.__course_list.values()


    def get_degree(self, degree_name):
        return self.__degree_list.get(degree_name, "")


    # There are three course objects being used here:
    # 1) a default course object
    # 2) a target course with ONLY the attributes we want to require changed to their required states
    # 3) the courses present in the catalog
    # We first compare if the target course attribute is equal to the default value. If not, then we check
    # to see if the course in the catalog has that required value. If not, we pass it. If the course has all
    # the required values it will be added to the returned list
    def get_course_match(self, target_course):
        bundle = Bundle("Return", "CSCI", 0)
        default_course = Course("Default", "Default", 0)
        for course in self.__course_list.values():
            if target_course.name != default_course.name and target_course.name != course.name:
                continue
            if target_course.major != default_course.major and target_course.major != course.major:
                continue
            if target_course.level() != default_course.level() and target_course.level() != course.level():
                continue
            if target_course.credits != default_course.credits and target_course.credits != course.credits:
                continue
            if target_course.CI != default_course.CI and target_course.CI != course.CI:
                continue
            if target_course.HASS_inquiry != default_course.HASS_inquiry and target_course.HASS_inquiry != course.HASS_inquiry:
                continue
            if target_course.HASS_pathway != default_course.HASS_pathway and target_course.HASS_pathway != course.HASS_pathway:
                continue
            if target_course.concentration != default_course.concentration and target_course.concentration != course.concentration:
                continue
            if target_course.prerequisites != default_course.prerequisites and target_course.prerequisites != course.prerequisites:
                continue
            bundle.add(course)
        return bundle


    def to_string(self):
        count1 = 1
        printout = ""
        for course in self.__course_list.values():
            printout+=str(count1) + ": " + course.to_string() + "\n"
            count1+=1
        count1 = 1
        for degree in self.__degree_list.values():
            printout+=str(count1) + ": " + degree.to_string() + "\n"
            count1+=1
        return printout
