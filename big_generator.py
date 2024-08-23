import xml.etree.ElementTree as ExtraTerrestrial
import requests
import time
import csv
import os

last_res = input('What is the number of the last passed GA resolution? ')
user_name = input('Enter your nation name: ')

if not os.path.exists('repeals_cache.txt'):
	f = open('repeals_cache.txt', 'x')
	f.close()

print('Reading cache...')
f = open('repeals_cache.txt', 'r')
repeals_output = f.read()
repealed_reses = repeals_output.split(',')
f.close()

item = 1
while item <= int(last_res):
	if str(item) not in repealed_reses:
		print('Fetching data for GA #' + str(item) + '...')
		res_xml = ExtraTerrestrial.fromstring(requests.get('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&id=' + str(item) + '&q=resolution', headers={'User-Agent':'Committees script created by the Ice States and used by ' + user_name + ' : https://github.com/canineanimal/ga-committees'}).content)
		if (len(res_xml.findall('RESOLUTION/REPEALED')) == 1) or (res_xml.find('RESOLUTION/CATEGORY').text == 'Repeal'):
			repealed_reses.append(item)
			repeals_output += str(item) + ','
			print('GA #' + str(item) + ' recorded as repeal(ed).')
		time.sleep(0.6)
	else:
		print('Skipping GA #' + str(item) + ' as it is in cache')
	item += 1

print('Saving cache...')
f = open('repeals_cache.txt', 'w')
f.write(repeals_output)
f.close()

active_table = '[table][tr][td][b][align=center]Committee[/align][/b][/td][td][b][align=center]Parent[/align][/b][/td][td][b][align=center]Alternate Names[/align][/b][/td][td][b][align=center]References (active)[/align][/b][/td][td][b][align=center]References (repealed)[/align][/b][/td][/tr]'
repealed_table = '[table][tr][td][b][align=center]Committee[/align][/b][/td][td][b][align=center]Parent[/align][/b][/td][td][b][align=center]Alternate Names[/align][/b][/td][td][b][align=center]References (repealed)[/align][/b][/td][/tr]'

print('Generating table data...')
cf = open('committees.csv', 'r')
reader = csv.reader(cf)
found = False
rows = list(reader)
non_header_row = False
for row in rows:
	if non_header_row:
		active_mentions = ''
		repealed_mentions = ''
		jtem = 0
		for mention in row:
			if(jtem < 3):
				jtem += 1
			elif str(mention) in repealed_reses:
				if repealed_mentions == '':
					repealed_mentions = '[url=https://www.nationstates.net/page=WA_past_resolution/id=' + mention + '/council=1]GA #' + mention + '[/url]'
				else:
					repealed_mentions += ', [url=https://www.nationstates.net/page=WA_past_resolution/id=' + mention + '/council=1]GA #' + mention + '[/url]'
			else:
				if active_mentions == '':
					active_mentions = '[url=https://www.nationstates.net/page=WA_past_resolution/id=' + mention + '/council=1]GA #' + mention + '[/url]'
				else:
					active_mentions += ', [url=https://www.nationstates.net/page=WA_past_resolution/id=' + mention + '/council=1]GA #' + mention + '[/url]'
		
		if active_mentions == '':
			repealed_table += '[tr][td]' + row[0] + '[/td][td]' + row[1] + '[/td][td]' + row[2] + '[/td][td]' + repealed_mentions + '[/td][/tr]'
		else:
			active_table += '[tr][td]' + row[0] + '[/td][td]' + row[1] + '[/td][td]' + row[2] + '[/td][td]' + active_mentions + '[/td][td]' + repealed_mentions + '[/td][/tr]'
	else:
		non_header_row = True

repealed_table += '[/table]'
active_table += '[/table]'
cf.close()

print('Saving data...')
aw = open('active.txt', 'w')
aw.write(active_table)
aw.close()

rw = open('repealed.txt', 'w')
rw.write(repealed_table)
rw.close()

print('Process complete!')