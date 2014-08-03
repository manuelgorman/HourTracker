#!/usr/bin/python

import MySQLdb
import datetime

def findDay(input):
	days = ["null","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
	retThis = days[input]
	return(retThis)

def toBool(testBit):
	if testBit == 0:
		retThis = '<div style="display:inline;color:lime;">No</div>'
	else:
		retThis = '<div style="display:inline;color:red;">Yes</div>'
	return retThis

def stripDigs(time):
	lastIndex = str(time).rindex(":")
	outString = str(time)[:lastIndex]
	return outString

def convertDates(date):
	date = str(date)
	day = date[date.rindex("-") + 1:]
	month = date[date.index("-") + 1:date.index("-") + 3]
	year = date[:4]
	return """%s-%s-%s""" % (str(day), str(month), str(year))


def returnEarnedMonies(timeIn,wage):
        [hours, minutes, seconds] = [int(x) for x in str(timeIn).split(':')]
        secsOut = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
#        return secsOut.seconds
	final =(secsOut.seconds/3600 * wage)
	return final


db = MySQLdb.connect(host="localhost",
                        user="work",
                        passwd="letmelookatthehours!",
                        db="work")

cur = db.cursor()

cur.execute("SELECT * FROM hours ORDER BY date ASC LIMIT 1;")
#print "Content-Type: text/html\n"

fulldurat = 0

for x in cur.fetchall():
	day = findDay(x[0])
	date = convertDates(x[1])
	start = stripDigs(x[2])
	durat = stripDigs(x[3])
	fulldurat = x[3]
	end = stripDigs(x[4])
	susan = toBool(x[5])

print '''<div class="hover" id="day">%s</div><div id="date" class="hover">%s</div><div id="newline"><div id="start" class="hover" class="A">Start:<div class="B">%s</div></div><div id="duration" class="hover">Length:<div class="B">%s</div></div><div class="hover" id="end">End:<div class="B">%s</div></div><div class="hover" id="susan">Susan:<div class="B">%s</div></div><div class="hover" id="Earned">Earnings:<div class="B">%s</div></div></div>''' % (day, date, start, durat, end, susan, chr(163) + str(returnEarnedMonies(fulldurat,6.57)))
