from array import *
from discord.ext import commands

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