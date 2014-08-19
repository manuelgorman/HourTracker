#!/usr/bin/python

import datetime
import cgi
import MySQLdb
import json
import sys

import cgitb	#Turn on fancy debugging so that if it fucks up, you know how
cgitb.enable()

arguments = cgi.FieldStorage()	#Store HTTP GET arguments in 'arguments' variable

### MySQL server settings ###
host = "localhost"
uname = "work"
pword = "letmelookatthehours!"
db = "work"
query = "SELECT * FROM hours LIMIT %s" % (arguments['results'].value)

class Shift():
	"docstring"		#I know I'm a bad person
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
	def dictionary(self):	#Returns a formatted dictionary of the values for the instance
		dict = {}
		dict["date"] = self.date.strftime("%a %d %b %Y")					#Format to "[Short weekday] [Day of month] [Month] [Year]"
		dict["start"] = self.start.strftime("%I:%M %p")						#Format to "[12 hour time]:[Minute] [AM or PM]
		dict["duration"] = self.convToTime(self.duration).strftime("%H:%M")	#Format to "[24 hour time]:[Minute]" okay its kind of hacky because its a duration but who cares, i'm the only one that's going to use this anyway
		dict["end"] = self.end.strftime("%I:%M %p")							#Format to "[12 hour time]:[Minute] [AM or PM]
		dict["susan"] = self.susan											#Send a good ol' boolean
		dict["earned"] = str(self.earned)									#Send the amount you earn
		return dict															#Send the dictionary on its merry way

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

#Run the query and store results in 'rawShifts'
cursor.execute(query)
rawShifts = cursor.fetchall()

#Prepare empty list to be filled with shift objects
shifts = []

#Iterate through results making an instance of the Shift object and append each instance of the Shift object to the list of shifts I CALLED TOO MANY THINGS SHIFT OH GOD
for shift in rawShifts:
	shiftInstance = Shift(shift['date'],shift['start'],shift['end'],shift['susan'])
	shifts.append(shiftInstance)	#Append the object to the list

requestedOutput = str(arguments["type"].value).upper()	#Just being tidy!
	
if requestedOutput == "TABLE":	#Send a table in HTML if requested - will be deprecated shortly
	#generateTable(shifts)	I'll get to this bit later
	pass
	
elif requestedOutput == "JSON":
	JSONShiftList = []
	for shift in shifts:
		JSONShiftList.append(shift.dictionary())
	sys.stderr.write(str(JSONShiftList))
	print "Content-Type: text/plain"	#Plain text is following (actually JSON but they don't need to know that)
	print								#Blank line, end of headers
	print json.dumps(JSONShiftList)		#Excrete what is hopefully JSON to whoever wants it

