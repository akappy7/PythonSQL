# Helper functions
import csv
import psycopg2

varCharExceptions = ['WRKTIME']
floatExceptions   = ['SFWGT', 'GCDWORK', 'TRPMILES', 'X', 'XX', 'XXX', 'XXXX', 'XXXXX', 'Value']
def buildRelation(csvFile, columns, connection, relationName):
	csvFile.seek(0) #was having issues with file already being read through by other functions

	#file accesor for the Data CSV file
	fileReaderD = csv.DictReader(csvFile)

	#need specially formatted column names string for the query, this is dog shit practice
	formedColumns = columns[0] # Computed once so doesn't have to re-do
	for c in columns[1:]: # Already stuck in the first column name
		formedColumns = formedColumns + ', ' + c

	for row in fileReaderD:
		insertRow(columns, formedColumns, connection, row, relationName)

# Takes a list of column names, a connection object, 
#	a dictionary, and the relation name.
# Column names should be the same as the dictionary, otherwise something is wrong
#
# I can see problems arising from the fact python tends to use ' instead of "
#
# The methods I use here are absolute crap, but I didnt want to wade through the documentation
#	to find the official way to deal with arrays of arguments for the queries.
#

def insertRow(columns, formedColumns, connection, row, relationName):
	cur = connection.cursor()



	rowValues = []
	for c in columns:
		#generate a list of values from the dictionary. This method will preserve order specified by columns
		rowValues.append(autoCaste(c, row[c]))

	rowValues = str(rowValues)[1:-1] # want a specially formatted rowValues string, takes off the brackets
	try:
		query = "INSERT INTO " + relationName + " (" + formedColumns + ") VALUES (" + rowValues + ")"
		cur.execute(query)
	except:
		print query
		exit()

#Thanks stackoverflow
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Takes a column arg to check if the string is in the exceptions list
def autoCaste(c, s):
	try:
		if 'xx' in s or 'XX' in s or 'Not Available' in s:
			return 133742069 #I dont know why the fuckers used x's for these values
		if c in varCharExceptions:
			return s
		elif c in floatExceptions:
			return float(s)
		if is_int(s):
			return int(s)
		elif is_float(s):
			return float(s)
		else:
			return s
	except:
		print 'error: '
		print c
		print s
		exit()

# Will generate the string that goes between the parentheses in the CREATE TABLE query
# IE columnName type,
# once generated we could just put this string in a config file or something

def generateTableHeader(columns, csvFile):
	csvFile.seek(0) #was having issues with file already being read through by other functions
	csvDict = csv.DictReader(csvFile)
	csvDict = csvDict.next() #only need the first row. <- this may cause problems if there are conflicting values
	header  = ""

	#initialize header using first element in columns
	if is_int(csvDict[columns[0]]):
		header = columns[0] + " integer"
	else:
		header = columns[0] + " varchar"


	for c in columns[1:]: #skip first element since we already used it for initialization
		if c in varCharExceptions:
			header = header + ', ' + c + ' varchar'
		elif is_int(csvDict[c]):
			header = header + ', ' + c + ' bigint' #was having problems with overflow
		elif is_float(csvDict[c]) or c in floatExceptions:
			header = header + ', ' + c + ' float'
		else:
			header = header + ', ' + c + ' varchar'

	return header


