# Helper functions
import csv
import psycopg2

def buildRelation(csvFile, columns, connection, relationName):
	csvFile.seek(0) #was having issues with file already being read through by other functions

	#file accesor for the Data CSV file
	fileReaderD = csv.DictReader(csvFile)

	for row in fileReaderD:
		dictData = {}
		for c in columns:
			# Want to caste integers if possible since schema will be defined with ints and strings and floats
			if is_int(row[c]):
				dictData[c] = int(row[c])
			elif is_float(row[c]):
				dictData[c] = float(row[c])
			else:
				dictData[c] = row[c]
		insertRow(columns, connection, dictData, relationName)

# Takes a list of column names, a connection object, 
#	a dictionary, and the relation name.
# Column names should be the same as the dictionary, otherwise something is wrong
#
# I can see problems arising from the fact python tends to use ' instead of "
#
# The methods I use here are absolute crap, but I didnt want to wade through the documentation
#	to find the official way to deal with arrays of arguments for the queries.

def insertRow(columns, connection, row, relationName):
	cur = connection.cursor()

	#need specially formatted column names string for the query, this is dog shit practice
	formedColumns = columns[0] 
	for c in columns[1:]: # Already stuck in the first column name
		formedColumns = formedColumns + ', ' + c

	rowValues = []
	for c in columns:
		#generate a list of values from the dictionary. This method will preserve order specified by columns
		rowValues.append(row[c])

	rowValues = str(rowValues)[1:-1] # want a specially formatted rowValues string, takes off the brackets

	query = "INSERT INTO " + relationName + " (" + formedColumns + ") VALUES (" + rowValues + ")"
	cur.execute( query, (rowValues, ))

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


# Will generate the string that goes between the parentheses in the CREATE TABLE query
# IE columnName type,
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
		if is_int(csvDict[c]):
			header = header + ', ' + c + ' integer'
		elif is_float(csvDict[c]):
			header = header + ', ' + c + ' float'
		else:
			header = header + ', ' + c + ' varchar'

	return header


