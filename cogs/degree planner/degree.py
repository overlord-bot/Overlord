from array import *

class Degree():

    def __init__(self, name):
        self.name = name # name of the degree program
        self.list_and_rules = [] # list of List_and_rules objects that dictate requirements for this degree

        self.taken_course
        self.ntaken_course

    def add_core(self, course):
        i = len(self.core_course)
        while (i > 0):  # find the element in the list with the course major or loop to end
            if (self.core_course[i].get_title == course.major):
                break
            i-=1

        if not i:  # no such course bundle yet
            self.core_course.append(Bundle(course.major, course, course))
            self.core_course[-1].add(course)
        else:  # find the element of the major courses
            self.core_course[i].add(course)

        #use a hashmap, with course name as key and course bojet as value

    def remove_core(self, course):
        i = len(self.core_course)
        while (i > 0):  # find the element in the list with the course major or loop to end
            if (self.core_course[i].get_title() == course.major):
                break
            i-=1

        if i:
            self.core_course[i].remove(course)


    def recommend(self):
        for course_u in self.ntaken_course:
            level = course_u.level()

            for course_t in self.taken_course:
                cnt = 0
                if course_t in course_u.prerequisites:
                    ++cnt

            if level == 1:
                pass
                # recommend

            if level == 2:
                if cnt == len(course_u.prerequisites):  # 2000 level, all pre fulfilled
                    pass
                    # recommend
                else:  # 2000 level, not all fulfilled
                    pass
                    # recommend pre

            #if (level == 4):

        # use all the taken course, loop through utaken
        # if a course taken is a prerequisite of a utaken course

        # recommend all utaken 1000 level requirement

        # for the utaken course that is at 2000 level if all requirement is fulfilled, add to the list
        # for 2000 level course that is not yet fulfilled all, recommend the prerequisite of the course

        # 4000 level course generally have same prerequisite or none prerequisite
        # how to recommend, we cant recommend all 4000 level course at same time\
        # recommend courses as a bundle for different concentration
        # or if taken_course have 4000 level class, find the concentration bundle that have the most overlaps

        # minor can be treat as a class
        # pathway generally have a suggesting minor, which can be treat as a major

    def to_string(self):
        return self.name

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def __hash__(self):
        return hash(self.name)