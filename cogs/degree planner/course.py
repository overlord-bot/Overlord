from array import *

class Course():

    def __init__(self, name, major, cid):
        self.name = name
        self.major = major # major tag i.e. CSCI, ECSE
        self.course_id = cid # number of course, i.e. 1200, 2500
        self.credits = 0 # credit hours of this course
        self.cross_listed = [] # list of other courses that are cross listed and should be treated as identical to this one

        self.syllabus = dict() # this should be a dictionary of <professor, link>

        # critical attributes
        self.CI = False # if it's communication intensive
        self.HASS_inquiry = False # if it's hass inquiry
        self.HASS_pathway = "" # hass pathway this class belongs to, if none, will be ""
        self.concentration = "" # concentration area this class belongs to, if none, will be ""
        self.prerequisites = [] # a list of other classes that must be taken prior to this one
        self.suggested_prerequisites = [] # optional, will be displayed as a notification rather than a hard requirement
        self.restricted = False # if this is a major restricted class

        # optional attributes
        self.description = "" # text to be displayed describing the class
        self.not_fall = False # if this class is usually unavailable in fall semesters
        self.not_spring = False # if this class is usually unavailable in spring
        self.not_summer = False # if this class is usually unavailable in the summer


    
    def fall_only(self):
        self.not_fall = False
        self.not_spring = True
        self.not_summer = True

    def spring_only(self):
        self.not_fall = True
        self.not_spring = False
        self.not_summer = True

    def summer_only(self):
        self.not_fall = True
        self.not_spring = True
        self.not_summer = False

    # determines the level of the course, 1000=1, 2000=2, 4000=4, etc
    def level(self):
        return (self.course_id//1000)

    def to_string(self):
        return f"{self.name} {self.major} {str(self.course_id)}"

    def __eq__(self, other):
        if self.name == other.name and self.course_id == other.course_id:
            return True
        return False

    def __hash__(self):
        return self.course_id