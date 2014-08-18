import datetime
import cgi
import MySQLdb
import json

arguments = cgi.FieldStorage()	#Store HTTP GET arguments in 'arguments' variable

### MySQL server settings ###
host = "localhost"
uname = "work"
pword = "letmelookatthehours!"
db = "work"
query = "SELECT * FROM hours LIMIT %s" % (arguments['results'])

class Shift():
	def __init__(self,date,start,end,susan): #Acquire the values for an arbitrary shift
		self.date = date
		self.rawStart = start
		self.rawEnd = end
		if susan == 1:
			self.susan = True
		elif susan == 0:
			self.susan = False
				
	def convToTime(timedeltaObj):		#Do some fancy stuff I found on StackOverflow to get a datetime.time object from a datetime.timedelta object
		dt = datetime.datetime
		return (dt.min + timedeltaObj).time()
	def dictionary():	#Returns a dictionary of the values for any given instance
		dict = {}
		dict["date"] = self.date
		dict["start"] = self.start
		dict["duration"] = self.duration
		dict["end"] = self.end
		dict["susan"] = self.susan
		dict["earned"] = self.earned
		return dict
	
	start = convToTime(rawStart)	#Get a datetime object for the start and end times
	end = convToTime(rawEnd)
	duration = datetime.datetime.combine(self.date, self.end) - datetime.datetime.combine(self.date, self.start) #Get the difference between the two time (needs to be a datetime.datetime object for the subtraction, so just use the date of the shift)
	earned = round((duration.total_seconds() * 6.57) / 3600, 2) #Calculate earnings from the total seconds and round to 2 d.p.

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

#Prepare empty list to be filled with shift objects
shifts = []

#Run the query and store results in 'rawShifts'
cursor.execute(query)
rawShifts = cursor.fetchall()

#Iterate through results and append each shift object to the list I CALLED TOO MANY THINGS SHIFT OH GOD
for shift in rawShifts:
	shiftInstance = Shift(shift['date'],shift['start'],shift['end'],shift['susan'])
	shifts.append(shiftInstance)	#Append the object to the list

if arguments["type"] == "table":	#Send a table in HTML if requested
	generateTable(shifts)
elif arguments["type"] == "json":	#Send json data if requested
	JSONShiftList = []
	for shift in shifts:
		JSONShiftList.append(shift.dictionary())
	print "Content-Type: text/plain"	# Plain text is following (actually JSON but they don't need to know that)
	print								# blank line, end of headers
	json.dumps(JSONShiftList)