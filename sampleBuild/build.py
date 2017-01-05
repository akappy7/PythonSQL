import psycopg2
import csv
from helperFunctions import *
import sys

def readColumns(ar, colFile):
	for l in colFile:
		ar.append(l.rstrip())


def buildNTHSDatabase():

	pathToData   = '../Extraneous/Ascii/' # change as needed
	conn         = psycopg2.connect("dbname=postgres user=akap") #change as needed
	cur          = conn.cursor()
	
	# Open csv's
	houseCSV     = file(pathToData + 'HHV2PUB.CSV', 'r')
	dayCSV       = file(pathToData + 'DAYV2PUB.CSV', 'r')
	personCSV    = file(pathToData + 'PERV2PUB.CSV', 'r')
	vehicleCSV   = file(pathToData + 'VEHV2PUB.CSV', 'r')

	# Open columns files
	houseColFile   = file('./houseColumns', 'r')
	dayColFile     = file('./dayColumns', 'r')
	personColFile  = file('./personColumns', 'r')
	vehicleColFile = file('./vehicleColumns', 'r')

	#initialize column lists, read in columns from files
	houseColumns   = []
	dayColumns     = []
	personColumns  = []
	vehicleColumns = []

	readColumns(houseColumns, houseColFile)
	readColumns(dayColumns, dayColFile)
	readColumns(personColumns, personColFile)
	readColumns(vehicleColumns, vehicleColFile)

	#generate table headers, create tables. Keys or whatever can probably be added in manually later.
	houseHeader   = generateTableHeader(houseColumns, houseCSV)
	dayHeader     = generateTableHeader(dayColumns, dayCSV)
	personHeader  = generateTableHeader(personColumns, personCSV)
	vehicleHeader = generateTableHeader(vehicleColumns, vehicleCSV)

	cur.execute('CREATE TABLE house (' + houseHeader + ')')
	cur.execute('CREATE TABLE day (' + dayHeader + ')')
	cur.execute('CREATE TABLE person (' + personHeader + ')')
	cur.execute('CREATE TABLE vehicle (' + vehicleHeader + ')')

	# Read csvs and insert.
	buildRelation(houseCSV, houseColumns, conn, 'house')
	print 'house done'
	buildRelation(dayCSV, dayColumns, conn, 'day')
	print 'day done'
	buildRelation(personCSV, personColumns, conn, 'person')
	print 'person done'
	buildRelation(vehicleCSV, vehicleColumns, conn, 'vehicle')
	print 'vehicle done'

	#make changes to databse persistent
	conn.commit()

	#disconnect/close db
	cur.close()
	conn.close()

def buildEIADatabase():
	pathToData   = '../Data/' # change as needed
	conn         = psycopg2.connect("dbname=postgres user=akap") #change as needed
	cur          = conn.cursor()
	
	# Open csv's
	electricCSV       = file(pathToData + 'EIA_CO2_Electric_2014.csv', 'r')
	transportationCSV = file(pathToData + 'EIA_CO2_Transportation_2014.csv', 'r')
	mkwhCSV           = file(pathToData + 'EIA_MkWh_2014.csv', 'r')

	# Open columns files
	electricColFile       = file('./electricColumns', 'r')
	transportationColFile = file('./transportationColumns', 'r')
	mkwhColFile           = file('./mkwhColumns', 'r')

	#initialize column lists, read in columns from files
	electricColumns       = []
	transportationColumns = []
	mkwhColumns           = []

	readColumns(electricColumns, electricColFile)
	readColumns(transportationColumns, transportationColFile)
	readColumns(mkwhColumns, mkwhColFile)

	#generate table headers, create tables. Keys or whatever can probably be added in manually later.
	electricHeader       = generateTableHeader(electricColumns, electricCSV)
	transportationHeader = generateTableHeader(transportationColumns, transportationCSV)
	mkwhHeader           = generateTableHeader(mkwhColumns, mkwhCSV)

	cur.execute('CREATE TABLE electric (' + electricHeader + ')')
	cur.execute('CREATE TABLE transportation (' + transportationHeader + ')')
	cur.execute('CREATE TABLE mkwh (' + mkwhHeader + ')')

	# Read csvs and insert.
	buildRelation(electricCSV, electricColumns, conn, 'electric')
	print 'electric done'
	buildRelation(transportationCSV, transportationColumns, conn, 'transportation')
	print 'transportation done'
	buildRelation(mkwhCSV, mkwhColumns, conn, 'mkwh')
	print 'mkwh done'

	#make changes to databse persistent
	conn.commit()

	#disconnect/close db
	cur.close()
	conn.close()

if __name__ == "__main__":
	if sys.argv[1] == '0':
		buildNTHSDatabase()
	if sys.argv[1] == '1':
		buildEIADatabase()
