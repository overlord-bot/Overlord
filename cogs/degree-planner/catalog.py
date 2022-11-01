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
        self.__bundles = dict()
        self.lock = False

        self.build_templates()


    def add_course(self, course:Course):
        self.__course_list.update({course.name:course})


    def add_degree(self, degree:Degree):
        self.__degree_list.update({degree.name:degree})


    def get_course(self, course_name:str):
        return self.__course_list.get(course_name, "")


    def get_all_courses(self):
        return self.__course_list.values()


    def get_degree(self, degree_name:str):
        return self.__degree_list.get(degree_name, "")


    def get_bundle(self, bundle_name:str) -> set:
        return self.__bundles.get(bundle_name, None)

    
    # initializes default templates to use
    def build_templates(self) -> None:
        pass


    # default matching function, matches against entire catalog
    def get_course_match(self, target_course:Course) -> Bundle:
        return get_course_match_from_pool(target_course, self.__course_list)


    def to_string(self) -> str:
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


# Intakes a criteria of courses that we want returned
# For example, if target_course specifies a 2000 level CSCI course, then all 2000 level CSCI courses inside
# course_list is returned
#
# There are three course objects being used here:
# 1) a default course object
# 2) a target course with ONLY the attributes we want to require changed to their required states
# 3) the courses present in the catalog
#
# We first compare if the target course attribute is equal to the default value. If not, then we check
# to see if the course in the catalog has that required value. If not, we pass it. If the course has all
# the required values it will be added to the returned list. Only courses within course_list will be
# considered for returning.
def get_course_match_from_pool(target_course:Course, course_pool:set) -> Bundle:
    bundle = Bundle("return", "0000", 0)
    default_course = Course("default", "0000", 0)
    for course in course_pool.values():
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