Pytime
======

A simple Python timetable planner. In console mode, it allow create and manage a tast timetable and it create some stats.

Usage
======

1) View timetable
-----
Just launch the command:

    python timetable.py

2) Update content
-----
You have to modify the file 'timetable.xml'.

Nodes description:

- days: list of day nodes
- day: attributes[date], list of periods nodes
- periods: list of period nodes
- period: attributes[type]=(MORNING|MIDDAY|AFTERNOON|NIGHT), list of task nodes
- task: attributes[tags], tags can be separated by pipes "|", content represent a task
