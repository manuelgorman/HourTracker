#!/usr/bin/python

import MySQLdb
import datetime

def findDay(input):
        days = ["null","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        retThis = days[input]
        return(retThis)

def toBool(testBit):
        if testBit == 0:
                retThis = '<div style="display:inline;color:#75b775">No</div>'
        else:
                retThis = '<div style="display:inline;color:#c44242">Yes</div>'
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

def convertVals(listIn):
	listOut = []
#	print "listinvalue =" + str(listIn[0])
	listOut.append(findDay(listIn[0]))
	listOut.append(convertDates(listIn[1]))
	listOut.append(stripDigs(listIn[2]))
	listOut.append(stripDigs(listIn[3]))
	listOut.append(toBool(listIn[4]))
	return listOut

def returnDecimalSecsVal(timeIn):
	[hours, minutes, seconds] = [int(x) for x in str(timeIn).split(':')]
	secsOut = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
	return secsOut.seconds


db = MySQLdb.connect(host="localhost",
                        user="work",
                        passwd="letmelookatthehours!",
                        db="work")

cur = db.cursor()

cur.execute("SELECT day, date, start, duration, susan FROM hours ORDER BY date ASC LIMIT 5;")
#print "Content-Type: text/html\n"
print '<table class="hover"><bold><tr id="bottom"><td>Day</td><td>Date</td><td>Start Time</td><td>Duration</td><td>Susan</td><td>Earnings</td></tr></bold>'

results = cur.fetchall()

totalMoneyList = []

for x in results:
	print "<tr>"
	newList = convertVals(x)
	for y in newList:
		print "<td>" + str(y) + "</td>"
	hhmmss = x[3]
	money = str(returnDecimalSecsVal(x[3]) / 3600 * 6.57)
	totalMoneyList.append(money)
	print "<td>" + chr(163) + money + "</td>"
	print "</tr>"

print "<tr>"

totalMoney = 0

for day in totalMoneyList:
	totalMoney = totalMoney + float(day)	

for i in range(4):
	print "<td></td>"
print "<td>TOTAL:</td>"
print "<td>", chr(163), totalMoney, "</td>"
print "</tr>"
print "</table>"
