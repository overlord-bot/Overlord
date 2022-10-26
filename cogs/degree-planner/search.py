from .course import Course

class Search():


    def __init__(self, catalog):
        self.catalog_obj = catalog
        self.__course_index = dict()

    def initialize(self):
        print("0")
        self.catalog = self.catalog_obj.get_all_courses()
        print("1")
        print("printing catalog inside search: \n" + str(self.catalog))
        self.generate_index()
        

    #store all the data in a dictionary
    def generate_index(self):
        for course in self.catalog:
            print("2")
            name = course.name
            words = name.split(' ')
            for word in words:
                print("3: " + word)
                if len(word) < 3:
                    continue
                #this is add three letter key only
                word_key = word[0:3]
                print("wordkey: " + word_key)
                if(word_key not in self.__course_index.keys()):
                    self.__course_index.update({word_key:[name]})
                    continue
                self.__course_index[word_key].append(name)

    def search(self, msg):
        words = msg.split(' ')
        possible_courses = "none"
        for word_temp in words:
            word = word_temp[0:3]
            if len(word) > 2 and word not in self.__course_index.keys():
                print("not course found")
                return
            if type(possible_courses) is str:
                possible_courses = self.__course_index[word]
            else:
                for added_course in possible_courses:
                    if added_course not in self.__course_index[word]:
                        possible_courses.remove(added_course)
        print(str(possible_courses))
