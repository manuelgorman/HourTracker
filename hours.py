import datetime
import cgi
import MySQLdb

arguments = cgi.FieldStorage()	#Store HTTP GET arguments in 'arguments' variable

### MySQL server settings ###
host = "localhost"
uname = "work"
pword = "letmelookatthehours!"
db = "work"
	
class Shift():
	def __init__(self,date,start,end,susan): #Acquire the values for an arbitrary shift
		self.date = date
		self.rawStart = start
		self.rawEnd = end
		self.susan = susan
		
	def convToTime(timedeltaObj):		#Do some fancy stuff I found on StackOverflow to get a datetime.time object from a datetime.timedelta object
		dt = datetime.datetime
		return (dt.min + timedeltaObj).time()
	
	start = convToTime(rawStart)	#Get a datetime object for the start and end times
	end = convToTime(rawEnd)
	duration = datetime.datetime.combine(self.date, self.end) - datetime.datetime.combine(self.date, self.start) #Get the difference between the two time (needs to be a datetime.datetime object for the subtraction, so just use the date of the shift)
	earned = round((duration.total_seconds() * 6.57) / 3600, 2) #Calculate earnings from the total seconds and round to 2 d.p.
	
#Set up database connection
dbCon = MySQLdb.connect(host,uname,pword,db)
cursor = dbCon.cursor(MySQLdb.cursors.DictCursor)

if arguments["shifts"] == 1:
	
	
