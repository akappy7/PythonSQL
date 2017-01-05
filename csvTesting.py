import csv


dayFile     = file('./Extraneous/Ascii/DAYV2PUB.CSV', 'r')

dayReader     = csv.DictReader(dayFile)

for row in dayReader:
	print row['HOUSEID']
