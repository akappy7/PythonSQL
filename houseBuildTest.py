import psycopg2
import csv
from helperFunctions import *

conn = psycopg2.connect("dbname=postgres user=steve")
cur = conn.cursor()

#change as needed
houseCSV = file('./Ascii/HHV2PUB.CSV', 'r')
houseColFile = file('./houseColumns.text', 'r')

columns = []
for line in houseColFile:
	columns.append(line.rstrip())



tableHeader = generateTableHeader(columns, houseCSV)
print tableHeader

cur.execute('CREATE TABLE house (' + tableHeader + ')')

buildRelation(houseCSV, columns, conn, 'house')

#make changes to databse persistent
conn.commit()

#disconnect/close db
cur.close()
conn.close()