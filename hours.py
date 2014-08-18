#!/usr/bin/python

import datetime
import cgi
import MySQLdb
import json
import sys

import cgitb
cgitb.enable()

arguments = cgi.FieldStorage()	#Store HTTP GET arguments in 'arguments' variable

### MySQL server settings ###
host = "localhost"
uname = "work"
pword = "letmelookatthehours!"
db = "work"
query = "SELECT * FROM hours LIMIT %s" % (arguments['results'].value)

class Shift():
	def __init__(self,date,start,end,susan): #Acquire the values for an arbitrary shift
		self.date = date
		self.rawStart = start
		self.rawEnd = end
		if susan == 1:
			self.susan = True
		elif susan == 0:
			self.susan = False
		self.start = self.convToTime(start)
		self.end = self.convToTime(end)
		self.duration = datetime.datetime.combine(self.date, self.end) - datetime.datetime.combine(self.date, self.start) #Get the difference between the two time (needs to be a datetime.datetime object for the subtraction, so just use the date of the shift)
		self.earned = round((self.duration.total_seconds() * 6.57) / 3600, 2) #Calculate earnings from the total seconds and round to 2 d.p.
				
	def convToTime(self,timedeltaObj):		#Do some fancy stuff I found on StackOverflow to get a datetime.time object from a datetime.timedelta object
		dt = datetime.datetime
		return (dt.min + timedeltaObj).time()
	def dictionary(self):	#Returns a dictionary of the values for any given instance
		dict = {}
		dict["date"] = self.date
		dict["start"] = self.start
		dict["duration"] = self.duration
		dict["end"] = self.end
		dict["susan"] = self.susan
		dict["earned"] = self.earned
		return dict


class Table:
		newTable = "<table class=" + chr(34) + "hover" + chr(34) + ">"
		endTable = "</table>"
		newRow = "<tr>"
		newHeadRow = "<tr id=bottom>"
		endRow = "</tr>"
		newCol = "<td>"
		endCol = "</td>"

#Set up database connection and cursor
dbCon = MySQLdb.connect(host,uname,pword,db)
cursor = dbCon.cursor(MySQLdb.cursors.DictCursor)
sys.stderr.write("Database connection set up")

#Prepare empty list to be filled with shift objects
shifts = []

#Run the query and store results in 'rawShifts'
cursor.execute(query)
rawShifts = cursor.fetchall()

sys.stderr.write("Results obtained!")

#Iterate through results and append each shift object to the list I CALLED TOO MANY THINGS SHIFT OH GOD
for shift in rawShifts:
	shiftInstance = Shift(shift['date'],shift['start'],shift['end'],shift['susan'])
	shifts.append(shiftInstance)	#Append the object to the list

if str(arguments["type"].value).upper == "TABLE":	#Send a table in HTML if requested
	#generateTable(shifts)
	pass
elif str(arguments["type"].value).upper() == "JSON":
	JSONShiftList = []
	for shift in shifts:
		JSONShiftList.append(shift.dictionary())
	sys.stderr.write(str(JSONShiftList))
	print "Content-Type: text/plain"	# Plain text is following (actually JSON but they don't need to know that)
	print								# blank line, end of headers
	print json.dumps(JSONShiftList, default=dthandler)
	
	
