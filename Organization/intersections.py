import csv

def cross2(A, B):
	for i in set(A) & set(B):
		print i
	print '\n'

def cross3(A, B, C):
	return set(A) & set(B) & set(C)

def cross4(A, B, C, D):
	return set(A) & set(B) & set(C) & set(D)


#god i love sublime

dayFile     = file('./Ascii/DAYV2PUB.CSV', 'r')
houseFile   = file('./Ascii/HHV2PUB.CSV', 'r')
personFile  = file('./Ascii/PERV2PUB.CSV', 'r')
vehicleFile = file('./Ascii/VEHV2PUB.CSV', 'r')

dayList     = csv.DictReader(dayFile).fieldnames
houseList   = csv.DictReader(houseFile).fieldnames
personList  = csv.DictReader(personFile).fieldnames
vehicleList = csv.DictReader(vehicleFile).fieldnames


print('day cross house:')
cross2(dayList, houseList)

print('day, person:')
cross2(dayList, personList)

print('day, vehicle:')
cross2(dayList, vehicleList)

print('house, person:')
cross2(houseList, personList)

print('house, vehicle:')
cross2(houseList, vehicleList)

print('person, vehicle:')
cross2(personList, vehicleList)

