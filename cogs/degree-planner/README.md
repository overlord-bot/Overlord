# Degree Planning Module for Overlord

This is a tool to be used within discord that allows generating out schedules of one's curriculum at RPI, with requirement checking and automated suggestions based on user's preferences.


## Commands:

`!dp`: displays option menu 

(currently, the menu is as follows: 1: test, 2: load course data from files, 9: scheduling mode. It is possilbe other numbers will be used for temporary testing purposes

`!dp <#>`: directly runs option from menu

### Inside scheduling mode (all messages are assumed to be commands, so no ! or other prefixes needed):

`add, <semester #>, [list of course names separated by commas]` : add a course to schedule

`remove, <semester #>, [list of course names separated by commas]` : remove a course from schedule

`print` : displays the user's current active schedule that lists all selected courses under their semester numbers, and requirement checking reports

`reschedule` : changes the active schedule that is being modified

`exit` : exits the scheduling mode and user's messages will no longer be automatically be interpreted as commands


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