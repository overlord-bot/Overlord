# Calendar module for Overlord-Bot

This module is used to manage events and reminders for the server, and is currently in development.

## Commands (Old)

To use the old commands, type `!calendar_old` or `!calendar_old_timer` followed by the command. However, this is not recommend as it creates a server-wide txt file containing data.

`!calendar_old add <event> <MM/DD/YYYY>` will add an event for that date to the calendar.

`!calendar_old remove <event>` or `!calendar remove <MM/DD/YYYY>` will remove an event from the calendar.

`!calendar_old view <week/month>` will pull up a calendar visual with all the events within the time frame.

`!calendar_old clear` will clear the calendar of its data and its events.

`!calendar_old_timer <MM/DD/YYYY>` will set a timer for the specified date.

## Commands (New)

To use the new commands, type `!calendar` followed by the command.

`!calendar add <event> <MM/DD/YYYY>` will add an event for that date to the calendar.

`!calendar remove <MM/DD/YYYY>` will remove an event from the calendar.

`!calendar view` will pull up a calendar visual with all the events for the month.

`!calendar clear` will clear the calendar of its data and its events.

`!calendar edit date <old date> <new date>` will change the events of one day to another and remove the old date's events.

`!calendar edit /<event1> /<event2>` will change event1 to event2

`!calendar remind <date>` will set a reminder for date and send all events on the date.

## Plans for the Week:

Current plans for the week:

-Put finishing touches on any bugs/code and work on slides for presentation, and renamed/moved around old calendar model to its own folder.

## Development Plans

Currently, the calendar module is in development. The following features are planned for the future:

-Add a command to edit events. (Implemented)

-Reminder system, where users can specify the date/event. (Implemented basic version)

-View of a week, month, or year (In progress)

