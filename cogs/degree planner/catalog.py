from array import *
from discord.ext import commands

class Catalog():

    #catalog will  be a list of courses and degrees
    #also store graphs for further analysis and course prediction of free electives

    courses = []
    degrees = []

    def add_course(course):
        courses.append(course)

    def add_degree(degree):
        degrees.append(degree)