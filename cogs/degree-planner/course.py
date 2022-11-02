from array import *

class Course():

    def __init__(self, name, major, cid):
        self.name = name.strip().casefold()
        if len(major) != 4 and major != "":
            print("COURSE INITIALIZATION WARNING: major is not 4 characters for course " + self.name + ", setting to empty string")
            self.major = ""
        else:
            self.major = major # major tag i.e. CSCI, ECSE
        self.course_id = 0
        self.course_id2 = 0
        if isinstance(cid, str):
            if '.' in cid:
                split_num = cid.split('.')
                if len(split_num) == 2 and split_num[0].isdigit() and split_num[1].isdigit():
                    course_id = int(float(split_num[0]))
                    course_id2 = int(float(split_num[1]))
                else:
                    print("COURSE INITIALIZATION ERROR: 2 part ID not <int>.<int> for course " + self.name)
                    
            elif not cid.isdigit():
                print("COURSE INITIALIZATION WARNING: course number is not a number for course " + self.name)
            else:
                course_id = int(float(cid))
        elif isinstance(cid, int):
            self.course_id = cid
        else:
            print("COURSE INITIALIZATION WARNING: course number is not a number for course " + self.name)

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
        
        self.available_semesters = set() # if empty, means available in all semesters

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

    def add_available(self, semester:str) -> None:
        self.available_semesters.add(semester)

    def remove_available(self, semester:str) -> None:
        self.available_semesters.remove(semester)

    def is_available(self, semester:str) -> bool:
        return not self.available_semesters or semester.casefold() in self.available_semesters

    # determines the level of the course, 1000=1, 2000=2, 4000=4, etc
    def level(self):
        return (self.course_id//1000)

    def __repr__(self):
        st = (f"{self.name}: {self.major} {str(self.course_id)}{f'.{self.course_id2}' if self.course_id2 != 0 else ''}, {self.credits} credits {'(CI)' if self.CI else ''}"
            f"{f', concentrations: {str(self.concentration)}' if len(self.concentration) != 0 else ''}"
            f"{f', pathways: {str(self.HASS_pathway)}' if len(self.HASS_pathway) != 0 else ''}")
        return st.replace("set()", "none")

    def __eq__(self, other):
        if (self.name == other.name and self.course_id == other.course_id and self.major == other.major and
            self.CI == other.CI and self.concentration == other.concentration and self.HASS_pathway == other.HASS_pathway and
            self.credits == other.credits and self.HASS_inquiry == other.HASS_inquiry and self.cross_listed == other.cross_listed and
            self.restricted == other.restricted and self.prerequisites == other.prerequisites):
            return True
        return False

    def __hash__(self):
        return self.course_id + len(self.HASS_pathway)*10 + len(self.concentration)*100 + len(self.prerequisites)*1000