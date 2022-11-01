from array import *
from .course import Course
from .bundle import Bundle
from .catalog import *


class TRules():

    label = '' # label should explain what this rule is, i.e. "in-major core classes", "free electives", "HASS electives", etc
    
    #-------------------------------------------------------------------------------------------------
    # course_template usage:
    #
    # <Course template object : number of courses that need to fulfill this template>
    #
    # note: a course template is a course where fields that are filled in will be treated
    # as required attributes of target courses. This is used to search for all courses 
    # that fulfills the template's criteria.
    #
    # special cases: if template course is a bundle, then it will be treated as a disjunction,
    # as in any course that is inside the bundle counts.
    #
    # special cases: if a wildcard * is used for a field, it means that field may take on
    # any valid value, and if at least one value causes the template to be fulfilled, then
    # the template is considered fulfilled.
    #-------------------------------------------------------------------------------------------------
    course_templates = dict() 

    #########################################################################################
    # FULFILLMENT CALCULATIONS
    #########################################################################################

    def fulfillment(self, taken_bundle:Bundle):

        # Data structure of status_return: {unfulfilled template name : {attribute : value}}
        status_return = dict()

        # iterates through all the templates
        for template, required_count in self.course_templates.items():

            # 1) checks for courses within taken_bundle that fulfills this templated requirement
            fulfilled_courses = get_course_match_from_pool(template, taken_bundle.get_bundle_set())

            # 2) checks if a bundle is specified. If it is, enforces that all courses within
            # fulfilled_courses to be within the specified bundle within template
            if isinstance(template, Bundle):
                fulfilled_courses = [x for x in fulfilled_courses if x in template.get_bundle_set()]

            # 3) let's count how many courses were fulfilled and if it's enough :D
            

            '''
            if isinstance(template, Bundle):
                print("template " + template.name + " is a bundle")
                bundle_template = None
                fulfilled_courses = Bundle(template.name,"0000",0)
                # iterates through each course inside bundle
                for course in template.get_bundle_set():
                    # if a template is found (which has a default name rather than a course name),
                    # then apply template rules to all courses inside the bundle
                    if course.name == "default":
                        bundle_template = course
                    elif course in taken_bundle.get_bundle_set():
                        fulfilled_courses.add(course)
                # if template exists, filter out all courses that doesn't fulfill the template
                if bundle_template is not None:
                    fulfilled_courses = get_course_match_from_pool(bundle_template, fulfilled_courses)
                if len(fulfilled_courses) < required_count:
                    print("template " + template.name + " not fulfilled")
                    status_return.update({template.name:{
                        "required":required_count, 
                        "actual":len(fulfilled_courses),
                        "taken":fulfilled_courses}})
            '''

