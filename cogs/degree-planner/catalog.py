from array import *
from discord.ext import commands
import discord
import asyncio
import copy

from .course import Course
from .degree import Degree

class Catalog():

    def __init__(self):
        # catalog will  be a list of courses and degrees
        # TODO also store graphs for further analysis and course prediction of free electives
        self.__course_list = dict() # course name as key
        self.__degree_list = dict() # degree name as key
        self.lock = False

        self.build_templates()


    def add_course(self, course:Course):
        self.__course_list.update({course.name:course})


    def add_degree(self, degree:Degree):
        self.__degree_list.update({degree.name:degree})


    def get_course(self, course_name:str):
        return self.__course_list.get(course_name.casefold(), "")


    def get_all_courses(self):
        return self.__course_list.values()


    def get_degree(self, degree_name:str):
        return self.__degree_list.get(degree_name, "")


    # initializes default templates to use
    def build_templates(self) -> None:
        pass


    # matches against entire catalog
    def get_course_match(self, target_course:Course) -> set:
        return get_course_match(target_course, self.__course_list.values())


    def __str__(self) -> str:
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
# For example, if target_course specifies 2000 as course ID, then all 2000 level CSCI courses inside
# course_list is returned
#
# There are three course objects being used here:
# 1) a default course object
# 2) a target course with ONLY the attributes we want to require changed to their required states
# 3) course pool - the courses we want to select from
#
# If the target course attribute is not equal to the default value and the course from the pool 
# has that required value, it will be returned.
def get_course_match(target_course:Course, course_pool:set, possible_values=None, top=True) -> set:
    matched_pool = set()
    default_course = Course("", "", 0)

    # interpret wildcards

    # <template generated from wildcard : set of courses that fulfills it>
    matched_pools = dict()

    # determine all possible values only if it hasn't been computed already.
    # this is just to avoid recomputing it everytime we run this function
    if possible_values == None:
        possible_values = {"major":set(),"id":set(),"pathway":set(),"concentration":set()}
        for course in course_pool:
            possible_values["major"] = {course.major}.union(possible_values["major"])
            possible_values["id"] = {course.level()*1000}.union(possible_values["id"])
            possible_values["pathway"] = course.HASS_pathway.union(possible_values["pathway"])
            possible_values["concentration"] = course.concentration.union(possible_values["concentration"])

    print("possible val: " + str(possible_values))

    # pops the first wildcard we see and run get_course_match with every combination of that field LMAO
    if target_course.major == "*":
        for val in possible_values["major"]:
            target_course.major = val
            matched_pools.update(get_course_match(target_course, course_pool, possible_values, False))
    elif target_course.course_id == "*":
        for val in possible_values["id"]:
            target_course.course_id = val
            matched_pools.update(get_course_match(target_course, course_pool, possible_values, False))
    elif target_course.HASS_pathway == "*":
        for val in possible_values["pathway"]:
            target_course.HASS_pathway = {val}
            matched_pools.update(get_course_match(target_course, course_pool, possible_values, False))
    elif target_course.concentration == "*":
        for val in possible_values["concentration"]:
            print("val: " + val)
            target_course.concentration = {val}
            matched_pools.update(get_course_match(target_course, course_pool, possible_values, False))
    else:
        print("evaluating under template with concentration " + str(target_course.concentration))
        target_course_copy = copy.deepcopy(target_course)
        for course in course_pool:
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
            if target_course_copy not in matched_pools:
                matched_pools.update({target_course_copy:set()})
            matched_pools[target_course_copy].add(course)

    if top:
        if len(matched_pools) == 0:
            return set()
        if len(matched_pools) == 1:
            return matched_pools[target_course]
    return matched_pools