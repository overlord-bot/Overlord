from array import *
from ..utils.output import *
import json

import logging

class Course():

    def __init__(self, name, major, cid):
        self.display_name = name
        self.name = name
        self.major = major # major tag i.e. CSCI, ECSE
        self.course_id = cid
        self.course_id2 = 0
        self.credits = 0 # credit hours of this course
        self.cross_listed = set() # set of cross listed courses that should be treated as same course
        self.syllabus = dict() # this should be a dictionary of <professor, link>

        # critical attributes
        self.CI = False # if it's communication intensive
        self.HASS_inquiry = False # if it's hass inquiry
        self.HASS_pathway = set() # set of pathways
        self.concentration = set() # set of concentrations
        self.prerequisites = set() # set of prerequisites
        self.suggested_prerequisites = set() # optional, set will be displayed as a notification
        self.restricted = False # if this is a major restricted class

        # optional attributes
        self.description = "" # text to be displayed describing the clas
        self.available_semesters = set() # if empty, means available in all semesters

        self.validate_course_data()
        
        if name == "":
            self.name = ""
        else:
            self.name = f"{self.major.casefold()} {str(self.course_id)} {name.strip().casefold()}"
            self.name = self.name.replace(',', '')


    """ Some input data for courses may not be in the desired format. 

        For example, most courses have an ID in the form of ####, but some
        have ####.##. We separate the latter form into 
        courseid = #### (numbers prior to dot) and courseid2 = ## (after dot)
        
        All data is modified in place, no arguments and return necessary
    """
    def validate_course_data(self, output:Output=None) -> None:
        if output == None: output = Output(OUT.CONSOLE)
        if isinstance(self.course_id, str):
            if '.' in self.course_id:
                split_num = self.course_id.split('.')
                if len(split_num) == 2 and split_num[0].isdigit() and split_num[1].isdigit():
                    self.course_id = int(float(split_num[0]))
                    self.course_id2 = int(float(split_num[1]))
                else:
                    logging.error(f"COURSE PARSING: 2 part ID not <int>.<int> for course " + self.name)
                    
            elif not self.course_id.isdigit():
                logging.error(f"COURSE PARSING: course number is not a number for course " + self.name)
            else:
                self.course_id = int(float(self.course_id))
        elif not isinstance(self.course_id, int):
            logging.error(f"COURSE PARSING: course number is not a number for course " + self.name)

    def add_prerequisite(self, prereq) -> None:
        self.prerequisites.add(prereq)

    def add_cross_listed(self, cross) -> None:
        self.cross_listed.add(cross)

    def in_pathway(self, pathway) -> bool:
        return pathway in self.HASS_pathway

    def add_pathway(self, pathway) -> None:
        self.HASS_pathway.add(pathway)

    def in_concentration(self, concentration) -> bool:
        return concentration in self.concentration

    def add_concentration(self, concentration) -> None:
        self.concentration.add(concentration)

    def add_available(self, semester:str) -> None:
        self.available_semesters.add(semester)

    def remove_available(self, semester:str) -> None:
        self.available_semesters.remove(semester)

    def is_available(self, semester:str) -> bool:
        return not self.available_semesters or semester.casefold() in self.available_semesters

    # determines the level of the course, 1000=1, 2000=2, 4000=4, etc
    def level(self) -> int:
        return (self.course_id//1000)

    """
    Returns:
        course (OrderedDict): all course attributes within an ordered dictionary
            includes name, id, id2, major, credits, CI, HASS_inquiry, crosslisted,
            concentrations, pathways, presequisites, restricted, description.

            Some attributes will be omitted if empty, includes all attributes that
            are the form of a list or set.
    """
    def json(self) -> OrderedDict:
        course = OrderedDict()
        course.update({'name':self.name})
        course.update({'id':self.course_id})
        if self.course_id2 != 0:
            course.update({'id2':self.course_id2})
        course.update({'major':self.major})
        course.update({'credits':self.credits})
        course.update({'CI':self.CI})
        course.update({'HASS_inquiry':self.HASS_inquiry})
        if len(self.cross_listed):
            course.update({'crosslisted':list(self.cross_listed)})
        if len(self.concentration):
            course.update({'concentrations':list(self.concentration)})
        if len(self.HASS_pathway):
            course.update({'pathways':list(self.HASS_pathway)})
        if len(self.prerequisites):
            course.update({'prerequisites':list(self.prerequisites)})
        course.update({'restricted':self.restricted})
        course.update({'description':self.description})
        return json.dumps(course)

    def __repr__(self):
        st = (f"{self.display_name if self.display_name else 'None'}: {self.major if self.major else 'None'} " + \
            f"{str(self.course_id)}{f'.{self.course_id2}' if self.course_id2 != 0 else ''}, " + \
            f"{self.credits} credits{' (CI)' if self.CI else ''}" + \
            f"{f', concentrations: {str(self.concentration)}' if len(self.concentration) != 0 else ''}" + \
            f"{f', pathways: {str(self.HASS_pathway)}' if len(self.HASS_pathway) != 0 else ''}")
        return st.replace("set()", "none")

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        if (self.name == other.name and self.course_id == other.course_id and self.major == other.major and
            self.CI == other.CI and self.concentration == other.concentration and 
            self.HASS_pathway == other.HASS_pathway and self.credits == other.credits and 
            self.HASS_inquiry == other.HASS_inquiry and self.cross_listed == other.cross_listed and
            self.restricted == other.restricted and self.prerequisites == other.prerequisites):
            return True
        return False

    def __hash__(self):
        return self.course_id + len(self.HASS_pathway)*10 + len(self.concentration)*100 + len(self.prerequisites)*1000