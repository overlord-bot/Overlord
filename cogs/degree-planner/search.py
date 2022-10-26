from .course import Course
from .catalog import Catalog


class Search():


    def __init__(self, catalog):
        self.catalog_obj = catalog
        self.__course_index = dict()


    # updates catalog and generates new index
    # should be called everytime catalog gets updated
    def initialize(self):
        self.catalog = self.catalog_obj.get_all_courses()
        self.generate_index()
        

    # generates <course key name : [all possible courses' full name]>
    # where course key name is the first 3 letters of each of the words inside its name
    def generate_index(self):
        self.__course_index.clear()
        for course in self.catalog:
            name = course.name
            words = name.split(' ')

            for word in words:
                if len(word) < 3:
                    continue

                #this is add three letter key only
                word_key = word[0:3].casefold()
                if(word_key not in self.__course_index.keys()):
                    self.__course_index.update({word_key:[name]})
                else:
                    self.__course_index[word_key].append(name)


    # searches for possible courses based on msg, 
    # taking into account only words inside msg of 3 letters and above
    def search(self, msg):
        words = msg.split(' ')
        possible_courses = "none"

        # checks the first 3 letters of each word from the user input against __course_index
        # to see if there exists a set of courses that contains all the words' keys
        #
        # Example:
        # <"Alg" : [course1, course2]>
        # <"Int" : [course1, course3]>
        # If user input was "Int Alg" or "Intro Algorithms" (since only first 3 letters count), then we add course1 to possible_courses

        for word in words:
            if len(word) < 3:
                continue
            course_key = word[0:3]
            if course_key not in self.__course_index.keys():
                print("no courses found")
                return
            if type(possible_courses) is str:
                possible_courses = self.__course_index[course_key]
            else:
                possible_courses = [course for course in possible_courses if course in self.__course_index[course_key]]

        # go through possible_courses to now verify their entire name and ensure that they're within the user input
        for word in words:
            possible_courses = [course for course in possible_courses if word.casefold() in course.casefold()]
            print("iterated " + word + ", " + str(possible_courses))                    

        print("possible courses: " + str(possible_courses))
        return possible_courses
