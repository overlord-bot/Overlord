from array import *
from .course import Course


class Rules():

    label = '' # label should explain what this rule is, i.e. "in-major core classes", "free electives", "HASS electives", etc
    course_list = set()
    min_courses = 0
    min_2000_courses = 0
    min_4000_courses = 0
    min_CI = 0
    required_courses = set()
    min_same_concentration = 0
    min_same_pathway = 0


    #########################################################################################
    # HELPER FUNCTIONS
    #########################################################################################

    # finds the longest set within dictionary values
    def longest(self, main_list):
        i = 0
        longest_path = set()
        for path in main_list.values():
            if i < len(path):
                i = len(path)
                longest_path = path
                
        return longest_path

    # finds the key with the longest set as a value
    def longest_names(self, main_list):
        i = 0
        longest_path_names = set()
        for path_name in main_list.keys():
            if i < len(main_list[path_name]):
                i = len(main_list[path_name])
                longest_path_names = {path_name}
            elif i == len(main_list[path_name]):
                longest_path_names.add(path_name)
                
        return longest_path_names


    #########################################################################################
    # FULFILLMENT CALCULATIONS
    #########################################################################################

    # returns fulfillment status, data format is <fulfillment category : <data category: data value>>
    # data category includes: "fulfilled", "required_amount", "actual_amount", "details"
    def fulfillment(self) -> dict():
        courses = 0
        courses_2k = 0
        courses_4k = 0
        courses_CI = 0
        required_copy = self.required_courses
        same_concentration = dict()
        same_pathway = dict()

        status_return = dict() # status that is returned

        for course in self.course_list:

            # counts required course amounts and required courses
            courses+=1
            if course.level() == 2:
                courses_2k+=1
            if course.level() == 4:
                courses_4k+=1
            if course.CI:
                courses_CI+=1
            if course in required_copy:
                required_copy.remove(course)

            # generates a dictionary of <pathway : [courses]> in same_pathway
            for pathway in course.HASS_pathway:
                if pathway in same_pathway:
                    existing_list = same_pathway.get(pathway)
                    existing_list.add(course)
                    same_pathway.update({pathway:existing_list})
                else:
                    same_pathway.update({pathway:{course}})

            # generates a dictionary of <concentration : [courses]> in same_concentration
            for concentration in course.concentration:
                if concentration in same_concentration:
                    existing_list = same_concentration.get(concentration)
                    existing_list.add(course)
                    same_concentration.update({concentration:existing_list})
                else:
                    same_concentration.update({concentration:{course}})

        # course fulfillment
        if (courses < self.min_courses):
            status_return.update({"min_courses":{"fulfilled":False , "required":self.min_courses, "actual":courses}})

        if (courses_2k < self.min_2000_courses):
            status_return.update({"min_2000_courses":{"fulfilled":False , "required":self.min_2000_courses, "actual":courses_2k}})

        if (courses_4k < self.min_4000_courses):
            status_return.update({"min_4000_courses":{"fulfilled":False , "required":self.min_4000_courses, "actual":courses_4k}})

        if (courses_CI < self.min_CI):
            status_return.update({"min_CI":{"fulfilled":False , "required":self.min_CI, "actual":courses_CI}})

        for c in required_copy:
            status_return.update({"required_course":{"fulfilled":False , "required":c}})

        if (len(self.longest(same_concentration)) < self.min_same_concentration):
            status_return.update({"min_same_concentration":{
                "fulfilled":False, 
                "required":self.min_same_concentration, 
                "actual":len(self.longest(same_concentration)),
                "longest_concentrations":self.longest_names(same_concentration),
                "all_concentrations":same_concentration}})

        if (len(self.longest(same_pathway)) < self.min_same_pathway):
            status_return.update({"min_same_pathway":{
                "fulfilled":False, 
                "required":self.min_same_pathway, 
                "actual":len(self.longest(same_pathway)),
                "longest_pathways":self.longest_names(same_pathway),
                "all_pathways":same_pathway}})

        return status_return


    # returns a formatted message instead of a dictionary, use this for easy debugging
    def fulfillment_return_message(self) -> str:
        status = self.fulfillment()
        status_return = ""

        for status_entry_name, status_entry in status.items():
            if status_entry_name == "min_courses":
                status_return += f"Minimum course number not met: {status_entry['actual']} of minimum {status_entry['required']} taken for {self.label}\n"

            if status_entry_name == "min_2000_courses":
                status_return += f"Minimum course number not met: {status_entry['actual']} of minimum {status_entry['required']} 2000 level couress taken for {self.label}\n"
        
            if status_entry_name == "min_4000_courses":
                status_return += f"Minimum course number not met: {status_entry['actual']} of minimum {status_entry['required']} 4000 level couress taken for {self.label}\n"

            if status_entry_name == "min_CI":
                status_return += f"Minimum CI not met: {status_entry['actual']} of minimum {status_entry['required']} CI couress taken for {self.label}\n"

            if status_entry_name == "required_course":
                status_return += f"Required course not taken: {status_entry['required']}\n"

            if status_entry_name == "min_same_concentration":
                status_return += f"Minimum {status_entry['required']} courses needed in the same concentration.\n"
                status_return += f"Your longest concentrations are {str(status_entry['longest_concentrations'])} of size {status_entry['actual']}\n"
                           
            if status_entry_name == "min_same_pathway":
                status_return += f"Minimum {status_entry['required']} courses needed in the same pathway.\n"
                status_return += f"Your longest pathways are {str(status_entry['longest_pathways'])} of size {status_entry['actual']}\n"

        return status_return


    # returns boolean if this rule is fulfilled
    def fulfilled(self) -> bool:
        return not len(self.fulfillment())


    
