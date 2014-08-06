#!/usr/bin/python

#Script to generate table of next 5 shifts

import sys
import MySQLdb
import datetime		#If these need explaining, you need to (re)learn python....
from shiftCore import shiftCore

host = "localhost"		#MySQL server hostname
uname = "work"			#Username
pword = "letmelookatthehours!"	#Password	
db = "work"			#Database to connect to
query = "SELECT date, start, end, susan FROM hours ORDER BY date ASC LIMIT 5;"	#Query to run against the MySQL database
dFormat = "%d %b %Y"	#Format of date to print
tFormatA = "%I:%M %p"	#Format of actual time, not duration
rate = 6.57	#How much you're paid/hour



#TABLE HEADERS
headers = ["Day", "Date", "Start Time", "Duration", "Susan", "Earned"]

def convToTime(timedeltaObj):		#Do some fancy stuff I found on StackOverflow to get a datetime.time object from a datetime.timedelta object
	val = timedeltaObj
	dt = datetime.datetime
	return (dt.min + val).time()

def genSusanCol(bool):
	if bool == 0:
		return shiftCore.table.newCol + "<div style=" + chr(34) + "display:inline;color:" + chr(35) + "75b775" + chr(34) + ">No</div>" + shiftCore.table.endCol
	elif bool == 1:
		return shiftCore.table.newCol + '<div style=' + chr(34) + "display:inline;color:" + chr(35) + "C44242" + chr(34) + ">Yes</div>" + shiftCore.table.endCol

def earned(secs):
	sys.stderr.write(str(secs.seconds) + "\n")
	mins = int(secs.seconds) / 60
	hours = mins / 60
	return (hours * rate)

def createDur(date, start, end):
	return datetime.datetime.combine(date, end) - datetime.datetime.combine(date, start)

def generateTable(shiftList):		#Function to create the whole table, nothing more, nothing less.
	print shiftCore.table.newTable		#Write the opening tag
	print shiftCore.table.newHeadRow		#Create the row for the headers
	for header in headers:		#Loop through the headers
		print shiftCore.table.newCol		#New column
		print header			#Write the header
		print shiftCore.table.endCol		#Close column
	print shiftCore.table.endRow		#End the headers row

	for shift in shiftList:			#Loop through the results from the MySQL query
		print shiftCore.table.newRow			#Create a new row every time a new set of results is looped to
		print shiftCore.table.newCol			#Create a new column
		print shift['date'].strftime("%A")	#Print the day of the week
		print shiftCore.table.endCol, shiftCore.table.newCol	#Close the last column and start another
		print shift['date'].strftime(dFormat)	#Write the date as specified in the variable
		print shiftCore.table.endCol, shiftCore.table.newCol	#Close the last column and start another
		startTime = convToTime(shift['start'])
		endTime = convToTime(shift['end'])
		print startTime.strftime(tFormatA)	#Print the start time
		print shiftCore.table.endCol, shiftCore.table.newCol	#Close the last column and start another
		dur = createDur(shift['date'], startTime, endTime)
		print str(dur) + shiftCore.table.endCol		#Print the duration and close the column
		print genSusanCol(shift['susan'])	#Print the whole susan column
		print shiftCore.table.newCol			#Start a new column
		print chr(163) + str(earned(dur))	#Print the amount earned for the shift

	print shiftCore.table.endTable

dbCon = MySQLdb.connect(host,uname,pword,db)
cur = dbCon.cursor(MySQLdb.cursors.DictCursor)
cur.execute(query)
results = cur.fetchall()
generateTable(results)
