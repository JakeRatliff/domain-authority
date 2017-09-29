from mozscape import Mozscape

client = Mozscape('mozscape-xxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

import csv
from urllib.parse import urlparse

import pygsheets
gc = pygsheets.authorize('client_secret.json')
sh = gc.open('Google Spreadsheet Name')
wks = sh.sheet1
wks5 = sh.worksheet('title', 'Sheet Title')

import time

def fetchGoogleSheet():
	numRows = len(wks5.get_col(1,returnas='matrix', include_empty=False))
	print('total rows is', numRows)
	sourceUrls = wks5.get_values((2,1),(numRows,1),returnas='matrix', majdim='ROWS', include_empty=False)
	return sourceUrls

data = fetchGoogleSheet()

with open('domainAuthorities.csv', 'a') as csvfile:
	fieldnames = ['domain', 'authority']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

def getDomains():
	domains = []
	for item in data:
		domain = urlparse(item[0]).netloc
		#domain = domain.replace('www.','')
		domains.append(domain)
	return domains

domains = getDomains()
domains = set(domains) #deduping
domains = list(domains)

def batchDomains():
	batchDomains = []
	newBatch = []
	count = 0
	for item in domains:
		newBatch.append(item)
		count = count + 1
		if count == 10:
			batchDomains.append(newBatch)
			count = 0
			newBatch = []
	return batchDomains

batchDomains = batchDomains()

print('\n\n...iterating list of', len(domains), 'domains for Moz DA....\n\n')

for item in batchDomains:
	domains = item
	try:
		metrics = client.urlMetrics(domains)
		for item in metrics:
			domain = item['uu']
			try:
				authority = item['pda']
				print(domain, authority)
				with open('domainAuthorities.csv', 'a') as csvfile:
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writerow({'domain':domain, 'authority': authority})
			except:
				print('exception encountered...')
				with open('domainAuthorities.csv', 'a') as csvfile:
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writerow({'domain':domain, 'authority': 'api exception'})
		time.sleep(10)
	except:
		for item in domains:
			print('exception encountered when trying to get urlMetrics for', item)
			with open('domainAuthorities.csv', 'a') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				writer.writerow({'domain':item, 'authority': 'ERROR'})
