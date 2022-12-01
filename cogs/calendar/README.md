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

`!calendarv2 edit date <old date> <new date>` will change the events of one day to another and remove the old date's events.

`!calendarv2 edit /<event1> /<event2>` will change event1 to event2

`!calendarv2 remind <date>` will set a reminder for date and send all events on the date.

## Plans for the Week:

Current plans for the week:

-Put finishing touches on any bugs/code and work on slides for presentation.

## Development Plans

Currently, the calendar module is in development. The following features are planned for the future:

-Add a command to edit events. (Implemented)

-Reminder system, where users can specify the date/event. (Implemented basic version)

-View of a week, month, or year (In progress)

