import csv

def writeList(f, l):
	for line in l:
		f.write(line + '\n')
	f.close()


pathToData   = '../Data/' # change as needed

electricColFile       = file('./electricColumns', 'w')
transportationColFile = file('./transportationColumns', 'w')
mkwhColFile           = file('./mkwhColumns', 'w')

# Open csv's
electricFile       = file(pathToData + 'EIA_CO2_Electric_2014.csv', 'r')
transportationFile = file(pathToData + 'EIA_CO2_Transportation_2014.csv', 'r')
mkwhFile           = file(pathToData + 'EIA_MkWh_2014.csv', 'r')



electricList       = csv.DictReader(electricFile).fieldnames
transportationList = csv.DictReader(transportationFile).fieldnames
mkwhList           = csv.DictReader(mkwhFile).fieldnames

writeList(electricColFile, electricList)
writeList(transportationColFile, transportationList)
writeList(mkwhColFile, mkwhList)

