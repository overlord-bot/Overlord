from array import *
import copy
import json

from .course import Course
from .degree import Degree
from .course_template import Template
from .search import Search
from ..utils.output import *

class Catalog():

    def __init__(self, name="main"):
        # catalog will be a list of courses and degrees
        # TODO also store graphs for further analysis and course prediction of free electives
        self.name = name
        self.output = Output(OUT.CONSOLE)
        self.__course_list = dict() # course name as key
        self.__degree_list = dict() # degree name as key

        self.search = Search()
        self.lock = False

        # search must be reindexed after modification to course list
        self.reindex_flag = False

    
    def reindex(self):
        self.search.update_items(self.__course_list.keys())
        self.search.generate_index()


    def add_course(self, course:Course):
        self.reindex_flag = True
        self.__course_list.update({course.name:course})

    
    def add_courses(self, courses:set):
        self.reindex_flag = True
        for c in courses:
            self.__course_list.update({c.name:c})


    def add_degree(self, degree:Degree):
        self.__degree_list.update({degree.name:degree})


    def add_degrees(self, degrees:set):
        for d in degrees:
            self.__degree_list.update({d.name:d})


    def get_course(self, course_name:str) -> Course:
        if self.reindex_flag:
            self.reindex()
            self.reindex_flag = False
        name = self.search.search(course_name.casefold())
        if len(name) == 1:
            return self.__course_list.get(name[0], None)
        else:
            self.output.print(f"CATALOG ERROR: catalog get course non unique course found: {str(name)}", OUT.ERROR)
        return None


    def get_all_courses(self):
        return self.__course_list.values()


    def get_all_course_names(self):
        return self.__course_list.keys()


    def get_degree(self, degree_name:str):
        return self.__degree_list.get(degree_name, None)


    def get_all_degrees(self):
        return self.__degree_list.values()


    """ Matches against entire catalog
    """
    def get_course_match(self, target_course:Course) -> dict:
        return get_course_match(target_course, self.__course_list.values())


    def get_best_course_match(self, target_course:Course) -> set:
        return get_best_course_match(target_course, self.__course_list.values())

    def json(self):
        catalog = dict()
        catalog.update({'courses':list(self.__course_list.keys())})
        catalog.update({'degrees':list(self.__degree_list.keys())})
        return json.dumps(catalog)

    def __repr__(self):
        count1 = 1
        printout = ""
        for course in self.__course_list.values():
            printout+=str(count1) + ": " + repr(course) + "\n"
            count1+=1
        count1 = 1
        for degree in self.__degree_list.values():
            printout+=str(count1) + ": " + repr(degree) + "\n"
            count1+=1
        return printout

    def __eq__(self, other):
        if not isinstance(other, Catalog):
            return False
        return self.get_all_courses() == other.get_all_courses()

    def __len__(self):
        return len(self.__course_list)


""" Intakes a criteria of courses that we want returned
    For example, if target_course specifies 2000 as course ID, then all 2000 level CSCI courses inside
    course_list is returned

    There are three course objects being used in this function:
    1) a default course object
    2) a target course with ONLY the attributes we want to require changed to their required states
    3) course pool - the courses we want to select from

    If the target course attribute is not equal to the default value and the course from the pool 
    has that required value, it will be returned.
"""
def get_course_match(target_course, course_pool:set, possible_values=None) -> dict:
    output = Output(OUT.CONSOLE)
    default_course = Course("", "", 0)

    # <template (may be generated from wildcard) : set of courses that fulfills it>
    matched_pools = dict()

    # finds union of template's available course pool and taken courses
    if isinstance(target_course, Template):
        if target_course.course_set:
            course_pool = target_course.course_set.intersection(course_pool)
        target_course = target_course.template_course

    if not isinstance(target_course, Course):
        output.print("CATALOG ERROR: get_course_match target_course is not instance of Course after initial call", OUT.ERROR)

    # makes a copy of target_course because it will be altered later on
    target_course = copy.deepcopy(target_course)

    # determine all possible values only if it hasn't been computed already.
    # this is just to avoid recomputing it everytime we run this function
    if possible_values == None:
        possible_values = {"major":set(),"id":set(),"pathway":set(),"concentration":set()}
        for course in course_pool:
            possible_values["major"] = {course.major}.union(possible_values["major"])
            possible_values["id"] = {course.level()*1000}.union(possible_values["id"])
            possible_values["pathway"] = course.HASS_pathway.union(possible_values["pathway"])
            possible_values["concentration"] = course.concentration.union(possible_values["concentration"])

    # pops the first wildcard we see and run get_course_match with every combination of that field LMAO
    if target_course.major == "*":
        for val in possible_values["major"]:
            target_course.major = val
            matched_pools.update(get_course_match(target_course, course_pool, possible_values))
    elif target_course.course_id == "*":
        for val in possible_values["id"]:
            target_course.course_id = val
            matched_pools.update(get_course_match(target_course, course_pool, possible_values))
    elif target_course.HASS_pathway == "*":
        for val in possible_values["pathway"]:
            target_course.HASS_pathway = {val}
            matched_pools.update(get_course_match(target_course, course_pool, possible_values))
    elif target_course.concentration == "*":
        for val in possible_values["concentration"]:
            target_course.concentration = {val}
            matched_pools.update(get_course_match(target_course, course_pool, possible_values))
    else:
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
            
            target_course_copy = copy.deepcopy(target_course)
            if target_course_copy not in matched_pools:
                matched_pools.update({target_course_copy:set()})
            matched_pools[target_course_copy].add(course)

    return matched_pools


def get_best_course_match(target_course, course_pool:set, possible_values=None) -> set:
    matched_pools = get_course_match(target_course, course_pool, possible_values)
    
    size = 0
    best_template = target_course
    best_fulfillment = set()
    for k, v in matched_pools.items():
        if len(v) > size:
            size = len(v)
            best_template = k
            best_fulfillment = v

    return best_fulfillment
