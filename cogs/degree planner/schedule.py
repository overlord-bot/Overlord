from array import *
from discord.ext import commands


class Schedule(commands.Cog, name="Degree Planner"):

    def __init__(self, bot):
        self.bot = bot

    async def setup(bot):
        await bot.add_cog(Schedule(bot))

    master_list = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        elif message.content.startswith("create course"):
            await message.channel.send("generating a course")
            course = Course()
            course.name = "data structures"
            await message.channel.send("created " + course.name)




class Course():

    #consistent properties unlikely to change
    name = ""
    major = "" #mjaor tag i.e. CSCI, ECSE
    course_id = 1 #number of course, i.e. 1200, 2500
    cross_listed = [] #list of other courses that are cross listed and should be treated as identical to this one

    CI = False #if it's communication intensive
    HASS_inquiry = False #if it's hass inquiry
    HASS_pathway = "" #hass pathway this class belongs to, if none, will be "none"
    concentration = "" #concentration area this class belongs to, if none, will be "none"
    prerequisites = [] #a list of other classes that must be taken prior to this one
    suggested_prerequisites = [] #optional, will be displayed as a notification rather than warning
    restricted = False #if this is a major restricted class

    #soft properties
    course_description = "" #text to be displayed describing the class
    course_syllabus = dict() #this should be a map of <professor, link>
    not_fall = False #if this class is usually unavailable in fall semesters
    not_spring = False #if this class is usually unavailable in spring
    not_summer = False #if this class is usually unavailable in the summer

    def fall_only():
        not_fall = False
        not_spring = True
        not_summer = True

    def spring_only():
        not_fall = True
        not_spring = False
        not_summer = True

    def summer_only():
        not_fall = True
        not_spring = True
        not_summer = False

    def level():
        return (course_id//1000)



class Catalog():

    #catalog will  be a list of courses and degrees
    #also store graphs for further analysis and course prediction of free electives

    courses = []
    degrees = []

    def add_course(course):
        courses.append(course)

    def add_degree(degree):
        degrees.append(degree)



class Degree():
    
    core = [] #list of courses absolutely required
    list_n_rules = [] #list of List_and_rules objects that dictate requirements
    


class Bundle(Course):
# A bundle represents a list of classes, can be treated as a course

    course_bundle = []

    def add_to_bundle(course):
        course_bundle.append(course)

    def __eq__(self, other):
        mylist = self.course_bundle
        otherlist = other.course_bundle

        for course in mylist:
            if course not in otherlist:
                return False
            otherlist.remove(course)
        if otherlist:
            return False
        return True



class List_and_rules():
# a list of classes and rules to determine the failure rate
# the failure rate is the number of classes that still needs to be added at a minimum to fulfill all the rules

    course_list = []
    min_courses = 0
    min_2000_courses = 0
    min_4000_courses = 0
    min_CI = 0
    required_courses = []
    min_same_concentration = 0
    min_same_pathway = 0

    def eval():
        courses = 0
        courses_2k = 0
        courses_4k = 0
        courses_CI = 0
        required_copy = required_courses
        same_concentration = dict()
        same_pathway = dict()

        for course in course_list:
            courses+=1
            if (course.level == 2):
                courses_2k+=1
            if (course.level == 4):
                courses_4k+=1
            if (course.CI):
                courses_CI+=1
            #TODO add pathway and concentration counter here
            if (course in required_copy):
                required_copy.remove(course)

        if (courses < min_courses or courses_2k < min_2000_courses or courses_4k < min_4000_courses or courses_CI < min_CI or required_copy):
            return False
        return True
