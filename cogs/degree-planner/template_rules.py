from array import *
from .course import Course
from .course_template import Template
from .catalog import *


class TRules():

    def __init__(self, name):

        # name should explain what this rule is, i.e. "in-major core classes", "HASS electives", etc
        self.name = name 

        #------------------------------------------------------------------------------------------------
        # course_template usage:
        #
        # <Course template object : number of courses that need to fulfill this template>
        #
        # note: a course template contains a course (called template_course) where fields 
        # that are filled in will be treated as required attributes of target courses. 
        # This is used to search for all courses that fulfills the template's criteria.
        #
        # If template course contains a course_set, then it will be treated as a disjunction,
        # as in courses must be selected from that pool of courses
        #
        # Wildcard * may be used for any field. This means that any value may be assigned for
        # that field but must remain consistent for all the courses (e.g. use wildcard to
        # specify if X amount of courses must be within the same pathway, but doesn't matter
        # which pathway)
        #-------------------------------------------------------------------------------------------------
        self.course_templates = dict()


    def add_template(self, template:Template, required_count):
        self.course_templates.update({template:required_count})


    def remove_template(self, template:Template):
        self.course_templates.pop(template)
    

    #########################################################################################
    # FULFILLMENT CALCULATIONS
    #########################################################################################

    def fulfillment(self, taken_courses:set):

        # Data structure of status_return: {unfulfilled template name : {attribute : value}}
        status_return = dict()

        # iterates through all the templates
        for template, required_count in self.course_templates.items():

            # 1) checks for courses within taken_bundle that fulfills this templated requirement
            fulfilled_courses = get_course_match(template.template_course, taken_courses)

            # 2) checks if lists are specified. If it is, enforces that all courses within
            # fulfilled_courses to be within the specified bundle within template
            if len(template.course_set):
                fulfilled_courses = [x for x in fulfilled_courses if x in template.get_bundle_set()]

            # 3) let's count how many courses were fulfilled and if it's enough :D
            if len(fulfilled_courses) < required_count:
                status_return.update({template.name:{"required":required_count, "actual":len(fulfilled_courses)}})


    # returns a formatted message instead of a dictionary, use this for easy debugging
    def fulfillment_return_message(self, taken_courses:set) -> str:
        status = self.fulfillment(taken_courses)
        status_return = ""

        for status_entry_name, status_entry in status.items():
            status_return += f"Template {status_entry_name} has unfulfilled courses: requires {status_entry['required']}, actual {status_entry['actual']}\n"

        return status_return


    def __repr__(self):
        return f"Template rule {self.name}: " 