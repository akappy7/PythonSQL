import psycopg2
import csv


def parseCSV(schemaFile, columnList):

    arrayData = []

    #file accesor for the Data CSV file
    fileReaderD = csv.DictReader(schemaFile)

    for row in fileReaderD:
        dictData = {}
        for c in columnList:
            dictData[c] = row[c]
        arrayData.append(dictData)

    return arrayData

arrayData = []
path = "1.txt"
#the actual csv file name
pathData = "./Data/EIA_CO2_Electric_2014.csv"

#file with the row by row of the collumns names that need to be put into the dictionary
schemaFile = file(pathData)

#creates an accesser to the file (schema)
fileReaderS = open(path, 'r')

for line in fileReaderS:
    arrayData.append(line.rstrip())


parseCSV(schemaFile, arrayData)

