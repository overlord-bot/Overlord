from array import *
from discord.ext import commands
import discord

from .output import *
from .course import Course
from .catalog import Catalog
from .degree import Degree
from .rules import Rule
from .schedule import Schedule
from .test_suite import Test1
from .user import User
from .user import Flag
from .search import Search
from .course_template import Template
from .command import *
from .parse import *


# just to help keep track of deployed versions without needing access to host
VERSION = "dev 11.1 (Revamped Parser)"
SEMESTERS_MAX = 12

class Degree_Planner(commands.Cog, name="Degree Planner"):
    """ DEGREE PLANNER COMMAND PARSER

    Receives commands and arguments separated by cammas in a string.
    Multiple commands allowed within one entry.

    Contains a Discord listener to automatically submit entries from
    Discord's chat.

    Valid commands are:
        (developer only)
        test
            - run test_suite.py
        import
            - parse course and degree information from json

        (general use)
        schedule, <schedule name>
            - set active schedule. New schedule will be created if
            specified schedule does not exist
        degree, <degree name>
            - set degree of active schedule
        add, <semester>, <course name>
            - add course to active schedule, courses may not duplicate
            within the same semester but may duplicate accross semesters
        remove, <semester>, <course name>
            - remove course from active schedule in specified semester
        print
            - print schedule
        fulfillment
            - print degree requirement fulfillment status
        find, <course>* (may list any number of courses)
            - find courses that match with the inputted string. Useful
            for browsing courses that contain certain keywords.

    NOTE: This class is created once and is not instigated for each user.
    It is essential to keep all user specific data inside the User class.

    """

    def __init__(self, bot):
        self.bot = bot

        # each user is assigned a User object and stored in this dictionary
        # Users = <user id, User>

        # note that the User object is meant to represent any user and does not
        # specifically have to be a discord user.
        self.users = dict()
        self.catalog = Catalog()
        self.course_search = Search()
        self.flags = set()

        self.title_delimiter = '---'


    """ Main message listener, passes the message content to helper functions

    Args:
        message (Discord message obj): contains message and relevant metadata
    """
    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        # ignore messages not from users
        if message.author == self.bot.user or message.author.bot:
            return

        # users from discord will be assigned user id equal to their discord id
        userid = str(message.author.id)
        if userid in self.users:
            user = self.users[userid]
            user.discord_user = message.author
            print(f"received msg from returning user: {message.author}, user id: {userid}")
        else:
            user = User(userid)
            user.username = str(message.author)
            user.discord_user = message.author
            self.users.update({userid:user})
            print(f"received msg from new user: {message.author}, user id: {userid}")

        output = Output(OUT.DISCORD_CHANNEL, 
            {ATTRIBUTE.USER:user, 
            ATTRIBUTE.CHANNEL:message.channel, 
            ATTRIBUTE.FLAG:ATTRIBUTE.EMBED})

        # only allows message through to message handler if there's a paused command
        # waiting for user input or if the message starts with !dp
        if Flag.CMD_PAUSED in user.flag:
            await self.message_handler(user, message.content, output)
            return

        if message.content.startswith('!dp '):
            await self.message_handler(user, message.content[4:], output)
            return


    """ MAIN FUNCTION FOR ACCEPTING COMMAND ENTRIES

    Args:
        user (User): user object containing all user data and unique user ID
        message (str): string to be parsed as command or submitted to a waiting
            active command
        output (Output): user interface output

    Returns:
        bool: whether input was successfully executed
    """
    async def message_handler(self, user:User, message:str, output:Output=None) -> bool:
        if output == None: output = Output(OUT.CONSOLE)
        if Flag.CMD_PAUSED in user.flag:
            user.command_queue_locked = True
            user.command_decision = message.strip().casefold()
        else:
            # if queue is available, immediately lock it and proceed
            if user.command_queue_locked:
                await output.print(f"ERROR{self.title_delimiter}queue busy, please try again later")
                return False
            user.command_queue_locked = True
            user.command_queue.join()
            commands = await self.parse_command(message, output)
            for command in commands:
                user.command_queue.put(command)
        await self.command_handler(user, output)
        user.command_queue_locked = False
        return True


    """ EXECUTES COMMANDS TAKEN FROM USER'S COMMAND QUEUE

    Args:
        user (User): user object containing all user data and unique user ID
        output (Output): user interface output
    """
    async def command_handler(self, user:User, output:Output=None) -> None:
        if output == None: output = Output(OUT.CONSOLE)
        output_debug = Output(OUT.CONSOLE)

        """
        This while loop will keep running until all commands are executed with
        one exception: if user input is requested to finish running a command.
        
        If that is the case, this loop will break, the current command will be 
        stored in User, and further user input will run this loop again where
        it first executes the stored command, and then continue as normal.
        
        NOTE: Use break to stop this loop only when awaiting user input
        and add Flag.CMD_PAUSED in user.flag, otherwise the loop can never
        be entered again.
        """
        while(not user.command_queue.empty() or Flag.CMD_PAUSED in user.flag):
            if Flag.CMD_PAUSED in user.flag:
                command:Command = user.command_paused
            else:
                command:Command = user.command_queue.get()

            if command.command == CMD.NONE:
                await output(f"ERROR{self.title_delimiter}there was an error understanding your command")
                user.command_queue.task_done()
                continue

            if command.command == CMD.TEST:
                await output_debug.print("BEGINNING TEST")
                await output.print(f"ADMIN{self.title_delimiter}Testing Degree Planner {VERSION}")
                await self.test(output_debug)
                await output_debug.print("FINISHED TEST")
                await output.print(f"ADMIN{self.title_delimiter}Test completed successfully, all assertions met")
                user.command_queue.task_done()
                continue

            if command.command == CMD.IMPORT:
                await output_debug.print("BEGINNING DATA IMPORTING")
                await output.print(f"ADMIN{self.title_delimiter}begin parsing data")
                await self.parse_data()
                await output_debug.print("FINISHED DATA IMPORTING")
                await output.print(f"ADMIN{self.title_delimiter}parsing completed")
                user.command_queue.task_done()
                continue

            if command.command == CMD.FIND:
                if len(command.arguments) == 0:
                    await output.print(f"FIND{self.title_delimiter}no arguments found. Use find, [courses] to find courses")
                else:
                    for entry in command.arguments:
                        await self.print_matches(entry, output)
                user.command_queue.task_done()
                continue

            if command.command == CMD.SCHEDULE:
                if not command.arguments:
                    await output.print(f"SCHEDULE{self.title_delimiter}not enough arguments, please specify a schedule name")
                else:
                    await self.set_active_schedule(user, command.arguments[0], output)
                user.command_queue.task_done()
                continue

            #------------------------------------------------------------------
            # all commands after this requires an active schedule inside User
            schedule = user.get_current_schedule()
            if schedule == None:
                await output.print(f"SCHEDULE{self.title_delimiter}no schedule selected")
                user.command_queue.task_done()
                continue
            #------------------------------------------------------------------


            if command.command == CMD.ADD or command.command == CMD.REMOVE:
                if Flag.CMD_PAUSED in user.flag:
                    decision = user.command_decision
                    courses = command.data_store
                    if not decision.isdigit() or int(decision) not in range(1, len(courses) + 1):
                        await output.print(f"SCHEDULE{self.title_delimiter}Please enter a valid selection number")
                        break
                    course:Course = courses[int(decision) - 1]
                    command.arguments[1] = course.name
                    user.flag.remove(Flag.CMD_PAUSED)

                semester = command.arguments[0]
                course = command.arguments[1]

                if command.command == CMD.ADD:
                    possible_courses = await self.add_course(user, course, semester, output)
                else:
                    possible_courses = await self.remove_course(user, course, semester, output)

                if possible_courses:
                    await output.print(f"@nomergeSCHEDULE{self.title_delimiter}entry {course} has multiple choices, please choose from list:")
                    i = 1
                    for c in possible_courses:
                        output.print_hold(f"{i}: {repr(c)}")
                        i += 1
                    await output.print_cache()
                    # pause command, set temporary variables/storage and break from the loop
                    command.data_store = possible_courses
                    user.command_paused = command
                    user.flag.add(Flag.CMD_PAUSED)
                    break

                user.command_queue.task_done()
                continue

            if command.command == CMD.PRINT:
                await output.print(f"@nomergeSCHEDULE{self.title_delimiter}{schedule.name}")
                output.print_hold(f"{str(schedule)}")
                await output.print_cache()
                user.command_queue.task_done()
                continue

            if command.command == CMD.DEGREE:
                if not command.arguments:
                    await output.print(f"SCHEDULE{self.title_delimiter}no arguments found. " + \
                        "Use degree, <degree name> to set your schedule's degree")
                else:
                    await self.set_degree(schedule, command.arguments[0], output)
                user.command_queue.task_done()
                continue

            if command.command == CMD.FULFILLMENT:
                if schedule.degree == None:
                    await output.print(f"SCHEDULE{self.title_delimiter}no degree specified")
                else:
                    await output.print(f"@nomergeSCHEDULE{self.title_delimiter}{schedule.name} Fulfillment")
                    output.print_hold(schedule.degree.fulfillment_msg(schedule.get_all_courses()))
                    await output.print_cache()
                user.command_queue.task_done()
                continue


    #--------------------------------------------------------------------------
    # HELPER FUNCTIONS
    #--------------------------------------------------------------------------

    
    """ Parse string into a list of Command objects

    Args:
        cmd (str): input string to be parsed
        output (Output): user interface output

    Returns:
        list[Command]: list of Command objects each containing data
            on command and arguments
    """
    async def parse_command(self, cmd:str, output:Output=None) -> list:
        if output == None: output = Output(OUT.CONSOLE)
        arg_list = [e.strip().casefold() for e in cmd.split(",") if e.strip()]
        cmd_queue = []
        last_command = None
        for e in arg_list:
            # if we find a command, push the last command to the queue and create new command
            if CMD.get(e) != CMD.NONE:
                if last_command != None:
                    cmd_queue.append(last_command)
                last_command = Command(e)
            # otherwise, add this as an argument to the last command
            else:
                if last_command != None:
                    last_command.arguments.append(e)
                else:
                    await output.print(f"ERROR{self.title_delimiter}invalid command '{e}'")
        # after exiting the loop, push the last command if it exists into the queue
        if last_command != None:
            cmd_queue.append(last_command)

        # validates all commands
        for e in cmd_queue:
            if not e.valid():
                await output.print(f"ERROR{self.title_delimiter}invalid arguments for command {str(e)}")
        cmd_queue = [e for e in cmd_queue if e.valid()]

        return cmd_queue

    
    """ Run test

    Args:
        output (Output): user interface output
    """
    async def test(self, output:Output=None):
        if output == None: output = Output(OUT.CONSOLE)
        test_suite = Test1()
        output.flags.add(Flag.DEBUG)
        await test_suite.test(output)
        output.flags.remove(Flag.DEBUG)


    """ Changes user's active schedule selection and creates new schedule if
        specified schedule is not found

    Args:
        user (User): user to perform the action on
        entry (str): schedule name
        output (Output): user interface output
    """
    async def set_active_schedule(self, user:User, entry:str, output:Output=None) -> None:
        if output == None: output = Output(OUT.CONSOLE)
        schedule = user.get_schedule(entry)
        if schedule == None:
            await output.print(f"SCHEDULE{self.title_delimiter}Schedule {entry} not found, generating new one!")
            user.new_schedule(entry)
            user.curr_schedule = entry
            return
        else:
            await output.print(f"SCHEDULE{self.title_delimiter}Successfully switched to schedule {entry}!")
            user.curr_schedule = entry
            return


    """ Changes user's active schedule's degree

    Args:
        user (User): user to perform the action on
        schedule (Schedule): schedule to change degree on
        entry (str): degree name
        output (Output): user interface output

    Returns:
        bool: if degree was successfully changed. 
            False usually means specified degree was not found
    """
    async def set_degree(self, schedule:Schedule, entry:str, output:Output=None) -> bool:
        if output == None: output = Output(OUT.CONSOLE)
        degree = self.catalog.get_degree(entry)
        if degree == None:
            await output.print(f"SCHEDULE{self.title_delimiter}invalid degree entered: {entry}")
            return False
        else:
            schedule.degree = degree
            await output.print(f"SCHEDULE{self.title_delimiter}set your degree to {degree.name}")
            return True


    """ Print list of courses that match input entry

    Args:
        entry (str): search term
        output (Output): user interface output
    """
    async def print_matches(self, entry:str, output:Output=None) -> None:
        if output == None: output = Output(OUT.CONSOLE)
        possible_courses = self.course_search.search(entry)
        await output.print(f"@nomergeFIND{self.title_delimiter}courses matching {entry}: ")
        i = 1
        for c in possible_courses:
            course = self.catalog.get_course(c)
            output.print_hold(f"  {i}: {course.major} {course.course_id} {course.display_name}")
            i += 1
        await output.print_cache()


    """ Add course to user's schedule

    Args:
        user (User): user to perform the action on
        entry (str): course name
        semester (int or str): semester to add course into
        output (Output): user interface output

    Returns:
        list: If there are multiple courses that match the input entry, then
            that list will be returned in the form of a list of Courses.
    """
    async def add_course(self, user:User, entry:str, semester, output:Output=None):
        if output == None: output = Output(OUT.CONSOLE)
        if isinstance(semester, str) and not semester.isdigit():
            await output.print(f"SCHEDULE{self.title_delimiter}semester must be a number")
            return False
        semester = int(semester)
        if semester not in range(0, SEMESTERS_MAX):
            await output.print(f"SCHEDULE{self.title_delimiter}Invalid semester {semester}, enter number between 0 and 11")
            return False
        
        returned_courses = [self.catalog.get_course(c) for c in self.course_search.search(entry)]

        if len(returned_courses) == 0:
            await output.print(f"SCHEDULE{self.title_delimiter}Course {entry} not found")
            return False
        elif len(returned_courses) > 1:
            return returned_courses
        
        course = returned_courses[0]
        user.get_current_schedule().add_course(course, semester)
        await output.print(f"SCHEDULE{self.title_delimiter}Added course {course.name} to semester {semester}")
        return False


    """ Remove course from user's schedule

    Args:
        user (User): user to perform the action on
        entry (str): course name
        semester (int or str): semester to remove course from
        output (Output): user interface output

    Returns:
        list: If there are multiple courses that match the input entry, then
            that list will be returned in the form of a list of Courses.
    """
    async def remove_course(self, user:User, entry:str, semester, output:Output=None):
        if output == None: output = Output(OUT.CONSOLE)
        if isinstance(semester, str) and not semester.isdigit():
            await output.print(f"SCHEDULE{self.title_delimiter}semester must be a number")
            return False
        semester = int(semester)
        if semester not in range(0, SEMESTERS_MAX):
            await output.print(f"SCHEDULE{self.title_delimiter}Invalid semester {semester}, enter number between 0 and 11")
            return False
        
        this_semester_courses = user.get_current_schedule().get_semester(semester)

        if len(this_semester_courses) == 0:
            await output.print(f"SCHEDULE{self.title_delimiter}No courses in semester {semester}")
            return False
        
        semester_course_search = Search(this_semester_courses, True)
        returned_courses = [self.catalog.get_course(c) for c in semester_course_search.search(entry)]

        if len(returned_courses) == 0:
            await output.print(f"SCHEDULE{self.title_delimiter}Course {entry} not found")
            return False
        elif len(returned_courses) > 1:
            return returned_courses
        
        course = returned_courses[0]
        user.get_current_schedule().remove_course(course, semester)
        await output.print(f"SCHEDULE{self.title_delimiter}Removed course {course.name} from semester {semester}")
        return False

    
    """ Parse json data into a list of courses and degrees inside a catalog

    Args:
        output (Output): user interface output

    Returns:
        Exception: if exception occurs, returns exception, else None
    """
    async def parse_data(self, output:Output=None) -> Exception:
        if output == None: output = Output(OUT.CONSOLE)
        output.flags.add(Flag.DEBUG)
        # redirects user messages into terminal, too much data for discord chat

        catalog_file = "catalog_results.json"
        degree_file = "class_results.json"

        try:
            await parse_courses(catalog_file, self.catalog, output)
            await output.print(f"ADMIN{self.title_delimiter}Sucessfully parsed catalog data")
            
            # set up searcher for finding courses based on incomplete user input
            self.course_search.update_items(self.catalog.get_all_course_names())
            self.course_search.generate_index()

            await parse_degrees(degree_file, self.catalog, output)
            await output.print(f"ADMIN{self.title_delimiter}Sucessfully parsed degree data, printing catalog")
            output.print_hold(str(self.catalog))
            await output.print_cache()

        except Exception as e:
            output.flags.remove(Flag.DEBUG)
            await output.print(f"ERROR{self.title_delimiter}An exception has occurred during parsing: {e}")
            return e

        else:
            output.flags.remove(Flag.DEBUG)
            return None


async def setup(bot):
    await bot.add_cog(Degree_Planner(bot))
