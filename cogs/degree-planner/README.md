# Degree Planning Module for Overlord

This is a tool to be used within Discord that allows generating out schedules of one's curriculum at RPI, with requirement checking and automated suggestions based on the user's preferences.


## Commands:

Commands can be chained together (i.e. !dp add, 1, data structures, remove, 1, data structures, print)
The only requirement is that '!dp' must be present at the very beginning when entering the command from Discord chat.

`schedule, <schedule name>` : changes the active schedule that is being modified

`degree, <degree name>` : assigns the specified degree to the current schedule for requirement checking purposes

`add, <semester #>, <course name>` : add a course to schedule

`remove, <semester #>, <course name>` : remove a course from schedule

`print` : displays the user's current active schedule that lists all selected courses under their semester numbers, and requirement checking reports

`fulfillment` : displays fulfillment status for degree requirements

Admin only:

`test` : runs test suite

`import` : imports json catalog into a Catalog object


## Class Structure:

user 
    - stores user data and user schedules
    
catalog 
    - stores one copy of RPI's course catalog and degree list
    - course_match to locate courses with a defined criteria
    
schedule
    - stores courses organized by semester

course
    - all data describing a course
    
degree
    - list of rules that describe degree requirements

course_template
    - describes criteria for filtering courses
    
rule
    - a set of course templates and the required fulfillment amount
    - fulfillment returns a dictionary of unfulfilled templates and its status/metadata
