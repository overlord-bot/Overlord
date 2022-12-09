from array import *
from .course import Course
from .course_template import Template
from .catalog import *
import json

class Rule():

    def __init__(self, name="Untitled rule"):
        self.name = name 

        """ course_template usage:
        
        <Template : number of courses that need to fulfill this template>
        
        note: a course template contains a course (called template_course) where fields 
        that are filled in will be treated as required attributes of target courses. 
        This is used to search for all courses that fulfills the template's criteria.
        
        If template course contains a course_set, then courses must be selected from 
        that pool of courses rather than the entire catalog.
        
        Wildcard * may be used for any field. This means that any value may be assigned for
        that field but must remain consistent for all the courses (e.g. use wildcard to
        specify if X amount of courses must be within the same pathway, but doesn't matter
        which pathway)
        """
        self.course_templates = dict()


    def add_template(self, template:Template, required_count=1):
        self.course_templates.update({template:required_count})


    def remove_template(self, template:Template):
        self.course_templates.pop(template)
    

    """
    Args:
        taken_courses (set): all courses the user have taken

    Returns:
        status_return (dict): returns fulfillment status in the form of
            <template name : <attribute : value>>
    """
    def fulfillment(self, taken_courses:set) -> dict:
        status_return = dict()

        for template, required_count in self.course_templates.items():

            # 1) checks for courses within taken_bundle that fulfills this templated requirement
            # return format is <template : {fulfilled courses}>
            fulfilled_courses = get_course_match(template, taken_courses)

            # 2) get biggest fulfillment within fulfilled_courses
            size = 0
            best_template = template
            best_fulfillment = set()
            for k, v in fulfilled_courses.items():
                if len(v) > size:
                    size = len(v)
                    best_template = k
                    best_fulfillment = v

            # 3) return fulfillment status
            status_return.update({template:{
                    "required":required_count, 
                    "actual":size,
                    "fulfilled":size >= required_count,
                    "fulfillment set":best_fulfillment,
                    "best_template":best_template}})

        return status_return


    """ 
    Returns:
        status_return (str): formatted message instead of a dictionary, use this for easy debugging
    """
    def fulfillment_return_message(self, taken_courses:set) -> str:
        status = self.fulfillment(taken_courses)
        status_return = ""

        if status != None:
            for template, data in status.items():
                status_return += f"{'' if data['fulfilled'] else '(UNFULFILLED)'} " + \
                    f"Template {template.name} status: \n  requires {data['required']}, " + \
                    f"actual {data['actual']},\n  fulfillment set: {str(data['fulfillment set'])}\n"

        return status_return


    """
    Returns:
        templates (dict): <template name : required course amount?
    """
    def json(self) -> dict:
        templates = dict()
        for k, v in self.course_templates.items():
            templates.update({k.name:v})
        return json.dumps(templates)

    def __repr__(self):
        s = f"rule {self.name}:\n" 
        for k, v in self.course_templates.items():
            s += f"  template {k.name} requires {v} counts: \n{str(k)}"
        return s

    def __eq__(self, other):
        if not isinstance(other, Rule):
            return False
        return self.course_templates == other.course_templates

    def __len__(self):
        return len(self.course_templates)

    def __hash__(self):
        i = 0
        for k, v in self.course_templates.items():
            i += hash(k) + v
        return i