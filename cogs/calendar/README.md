# Calendar module for Overlord-Bot

This module is used to manage events and reminders for the server, and is currently in development.

## Commands

To use the commands, type `!calendar` or `!calendar_timer` followed by the command. 

`!calendar add <event> <MM/DD/YYYY>` will add an event for that date to the calendar.

`!calendar remove <event>` or `!calendar remove <MM/DD/YYYY>` will remove an event from the calendar.

`!calendar view <week/month>` will pull up a calendar visual with all the events within the time frame.

`!calendar clear` will clear the calendar of its data and its events.

`!calendar_timer <MM/DD/YYYY>` will set a timer for the specified date.

### Development Plans
Currently, the calendar module is in development. The following features are planned for the future:
-Redesign of the calendar file, storing and reading from a json file instead of a text file.
-Fix remove command, currently does not work correctly with the events dictionary. (will change with the redesign)
-Add a command to edit events.
