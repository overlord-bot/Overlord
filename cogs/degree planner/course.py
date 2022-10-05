from array import *

class Course():

    def __init__(self, name, major, cid):
        self.name = name
        self.major = major # major tag i.e. CSCI, ECSE
        self.course_id = cid # number of course, i.e. 1200, 2500
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
        self.description = "" # text to be displayed describing the class
        self.not_fall = False # if this class is usually unavailable in fall semesters
        self.not_spring = False # if this class is usually unavailable in spring
        self.not_summer = False # if this class is usually unavailable in the summer

    def add_prerequisite(self, prereq):
        self.prerequisites.add(prereq)

    def add_cross_listed(self, cross):
        self.cross_listed.add(cross)

    def in_pathway(self, pathway):
        return pathway in self.HASS_pathway

    def add_pathway(self, pathway):
        self.HASS_pathway.add(pathway)

    def in_concentration(self, concentration):
        return concentration in self.concentration

    def add_concentration(self, concentration):
        self.concentration.add(concentration)

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
        st = (f"{self.name}: {self.major} {str(self.course_id)}, {self.credits} credits"
            f"{f', concentrations: {str(self.concentration)}' if len(self.concentration) != 0 else ''}"
            f"{f', pathways: {str(self.HASS_pathway)}' if len(self.HASS_pathway) != 0 else ''}")
        return st.replace("set()", "none")

    def __eq__(self, other):
        if self.name == other.name and self.course_id == other.course_id:
            return True
        return False

    def __hash__(self):
        return self.course_id