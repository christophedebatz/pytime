#!/usr/bin/env python
#coding: utf8 

from __future__ import print_function

'''
 Author: M. Christophe de Batz, software engineer

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import os
import os.path
import string
from decimal import Decimal
from xml.dom.minidom import parse, Node

HEADER  = '\033[95m' if os.name != 'nt' else u''
OKBLUE  = '\033[94m' if os.name != 'nt' else u''
OKGREEN = '\033[92m' if os.name != 'nt' else u''
WARNING = '\033[93m' if os.name != 'nt' else u''
ENDC    = '\033[0m'  if os.name != 'nt' else u''
BOLD    = '\033[1m'  if os.name != 'nt' else u''


def print_task_tags(task_node, color):
    tags = ()
    if task_node.hasAttribute('tags'):
	print (HEADER if color else ENDC, end='')
        print ("     |  Tags: ", end='')
        tags = task_node.getAttribute('tags').split('+')
        
        i = 0
	tags_length = len(tags)
        for index, value in enumerate(tags):
            print (value.capitalize(), end='')
            print ("{}".format(", ") if i == tags_length - 2 else "", end='')
	    i += 1


def load_xml_file(xml_filename):	
    if os.path.isfile(xml_filename) and os.access(xml_filename, os.R_OK):
        print (OKGREEN + " Accessing to " + xml_filename + " file..." + ENDC + os.linesep)
    else:
        sys.exit(" Error: cannot access to " + xml_filename + " file !")

    try:
        dom = parse(xml_filename)
    except Exception as e:
        sys.exit(" Error: " + str(e))
    
    return dom


def display_timetable(xml_filename):
    days = load_xml_file(xml_filename).getElementsByTagName('day')

    if len(days) <= 0:
        sys.exit(" Error: no records !")

    completed_tasks = 0

    for day in days:
        date = day.getAttribute('date')
        print (BOLD + " |-------------------- " + date + " --------------------" + ENDC + os.linesep)
        
        periods = day.getElementsByTagName('period')   
        
        for period in periods:
            type  = period.getAttribute('type') 
            tasks = period.getElementsByTagName('task')
            nb_tasks = len(tasks)
            completed_tasks += nb_tasks

	    print (OKBLUE + "   |- " + type.capitalize())
            print ("      " + str(nb_tasks) + " completed task(s)" if nb_tasks > 0 else "      No task for this period...")
            print (ENDC)

            i = 0
            for task in tasks:
                node = task.firstChild

                if node and node.nodeType == Node.TEXT_NODE:
                    print ("     |- " + node.nodeValue if i % 2 != 0 else HEADER + "     |- " + node.nodeValue + ENDC)
                    print_task_tags(task, i % 2 == 0)
		    print (ENDC, end='')
		else:
                    print (WARNING + "     X- Unreadable task..." + ENDC)
                
		print (os.linesep)            
		i += 1
            
            print ()
   
    average_tasks = Decimal(completed_tasks) / Decimal(len(days))
    average_tasks_hour = Decimal(average_tasks) / Decimal(8)

    print (BOLD + WARNING + " |-  Stats" + ENDC + WARNING)
    print ("   |- Number of days        : {}".format(str(len(days))))
    print ("   |- Completed tasks       : {}".format(str(completed_tasks)))
    print ("   |- Average task per day  : {0:0.2f}".format(average_tasks))
    print ("   |- Average task per hour : {0:0.2f}".format(average_tasks_hour))
  
    print (os.linesep + ENDC + OKGREEN + " End of file. Thanks." + ENDC)

if __name__ == "__main__":
    print (os.linesep)
    print (BOLD + OKGREEN +  " WELCOME ON BOARD :-)" + ENDC)
    display_timetable('timetable.xml' if len(sys.argv) <= 1 else sys.argv[1])
    print (os.linesep)
