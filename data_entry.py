import csv
import os

if not os.path.exists('committees.csv'):
	f = open('committees.csv', 'w')
	f.write('Committee,Parent,Alternate Names,Resolutions,')
	f.close()

while input('Do you want to continue? [y/n] ') != 'n':
	command = input('What command do you want to enter? [[a]dd committee;\n                                   add [r]eference]] : ')
	if command == 'a':
		name = input('Enter the committee name. "World Assembly" should be abbreviated as "WA"; otherwise avoid abbreviations. British spelling preferred. ')
		number = input('What resolution creates this committee? (Enter the resolution ID, eg 666 for GA #666, only.) ')
		alternate = input('Does this committee have any alternate names? Leave blank if not. ')
		parent = input('Does this committee have a parent? Leave blank if not. ')
		f = open('committees.csv', 'a')
		f.write(name + ',' + parent + ',' + alternate + ',' + number)
		f.close()
		print('Added!')
	elif command == 'r':
		name = input('Enter the committee name. Abbreviate World Assembly as "WA"; exclude abbreviations otherwise: ')
		number = input('What resolution references this committee? (Enter the resolution ID, eg 666 for GA #666, only.) ')
		alternate = input('Is the committee referenced by any alternate name? Leave blank if not. ')
		
		fr = open('committees.csv', 'r')
		reader = csv.reader(fr)
		found = False
		rows = list(reader)
		for row in rows:
			if row[0].lower() == name.lower():
				found = True
				row.append(number)
				if alternate != '':
					row[2] += ', ' + alternate
				
				fw = open('committees.csv', 'w')
				writer = csv.writer(fw)
				writer.writerows(rows)
				fw.close()
				
		if not found:
			print ('This committee does not appear to exist; please try again!')

		fr.close()				
	else:
		print ('This command does not seem to exist; avaiable options are \'a\' to [a]dd a committee, and \'r\' to add a [r]eference. Please try again...')

print('Data entry finished!')
