# Calendar module for Overlord-Bot

This module is used to manage events and reminders for the server, and is currently in development.

## Commands (Old)

To use the old commands, type `!calendar` or `!calendar_timer` followed by the command. 

`!calendar add <event> <MM/DD/YYYY>` will add an event for that date to the calendar.

`!calendar remove <event>` or `!calendar remove <MM/DD/YYYY>` will remove an event from the calendar.

`!calendar view <week/month>` will pull up a calendar visual with all the events within the time frame.

`!calendar clear` will clear the calendar of its data and its events.

`!calendar_timer <MM/DD/YYYY>` will set a timer for the specified date.

## Commands (New)

To use the new commands, type `!calendarv2` followed by the command.

`!calendarv2 add <event> <MM/DD/YYYY>` will add an event for that date to the calendar.

`!calendarv2 remove <MM/DD/YYYY>` will remove an event from the calendar.

`!calendarv2 view` will pull up a calendar visual with all the events for the month.

`!calendarv2 clear` will clear the calendar of its data and its events.

## Plans for the Week:

Current plans for the week:

Get new version to run properly with the new data managment system, as well as fix any bugs that may be present.

## Development Plans

Currently, the calendar module is in development. The following features are planned for the future:

-Redesign of the calendar file, storing and reading from a json file instead of a text file. (Implemented)

-Fix remove command, currently does not work correctly with the events dictionary. (Implemented)

-Add a command to edit events. (Ongoing)
